import torch, copy, cv2, math, os
import numpy as np
from scipy import stats
import signapse.constants as C
# from signapse.logo import LOGO
from torchvision import transforms 
from torch.autograd import Variable
import mediapipe as mp
mp_face_mesh = mp.solutions.face_mesh
from scipy.ndimage import shift, binary_fill_holes 
import matplotlib.pyplot as plt

def TM(frame, template_img):
    if len(template_img.shape) == 3:
        template_img = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)

    image_to_align = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Convert both images to grayscale
    image_to_align_gray = cv2.cvtColor(image_to_align, cv2.COLOR_BGR2GRAY)
    # Use template matching to find the location of the person in the image
    result = cv2.matchTemplate(image_to_align_gray, template_img, cv2.TM_CCOEFF_NORMED) 
    _, _, _, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    h, w = template_img.shape
    top_left = [top_left[0], top_left[1]]
    bottom_right = [top_left[0] + w, top_left[1] + h]
    centre = [(bottom_right[0] + top_left[0]) / 2, (bottom_right[1] + top_left[1]) / 2]
    # return top_left, bottom_right, centre
    return centre
    

# Draw a line between two points using OpenCV, if they are positive points
def draw_line(im, joint1, joint2, c=(0, 0, 255),t=1,width=3,decimal_places=2):
    thresh = 0
    joint1 = (round(joint1[0].item(), decimal_places), round(joint1[1].item(), decimal_places))
    joint2 = (round(joint2[0].item(), decimal_places), round(joint2[1].item(), decimal_places))
    if joint1[0] > thresh and  joint1[1] > thresh and joint2[0] > thresh and joint2[1] > thresh:
        center = (int((joint1[0] + joint2[0]) / 2), int((joint1[1] + joint2[1]) / 2))
        length = int(math.sqrt(((joint1[0] - joint2[0]) ** 2) + ((joint1[1] - joint2[1]) ** 2))/2)
        angle = math.degrees(math.atan2((joint1[0] - joint2[0]),(joint1[1] - joint2[1])))
        cv2.ellipse(im, center, (width,length), -angle,0.0,360.0, c, -1)
        
def draw_line_nonan(im, joint1, joint2, c=(0, 0, 255),t=1, width=3):
    if not (joint1.isnan().any() or joint2.isnan().any()):
        draw_line(im, joint1, joint2, c, t, width)
        
def draw_face_mesh_small_tensor(frame,FM_tensor,connections=mp_face_mesh.FACEMESH_TESSELATION):
    for connection in connections:
        start_idx = connection[0]
        end_idx = connection[1]

        start = (FM_tensor[start_idx][0].item(),FM_tensor[start_idx][1].item())
        end = (FM_tensor[end_idx][0].item(), FM_tensor[end_idx][1].item())

        cv2.line(frame, start,end,color=(1, 1, 1), thickness=1)
    return frame
        
# Convert from a tensor representation to an image
def tensor2im(image_tensor, imtype=np.uint8, normalize=True):
    if isinstance(image_tensor, list):
        image_numpy = []
        for i in range(len(image_tensor)):
            image_numpy.append(tensor2im(image_tensor[i], imtype, normalize))
        return image_numpy
    image_numpy = image_tensor.cpu().float().numpy()
    if normalize:
        image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 1) / 2.0 * 255.0
    else:
        image_numpy = np.transpose(image_numpy, (1, 2, 0)) * 255.0
    image_numpy = np.clip(image_numpy, 0, 255)
    if image_numpy.shape[2] == 1 or image_numpy.shape[2] > 3:
        image_numpy = image_numpy[:,:,0]
    return image_numpy.astype(imtype)     
            
class HEATMAPS():
    def __init__(self):
        super(HEATMAPS,self).__init__()
        
    def get_face_crop(self,MP_tensor, image,face_landmarks,box=False,gray = True, mouth_box = False, vertical_squeeze = -1):
        face_oval = list(mp_face_mesh.FACEMESH_FACE_OVAL)
        width, height = image.shape[1],image.shape[0]
        cropped_frame = np.zeros_like(image)

        if box:
            x_min, y_min = width, height
            x_max, y_max = 0, 0
            for landmark in face_landmarks:
                x, y = int(landmark[0] * width ), int(landmark[1] * height)
                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x)
                y_max = max(y_max, y)            
            cropped_frame[y_min:y_max, x_min:x_max] = image[y_min:y_max, x_min:x_max]
        elif mouth_box:
            x_min, y_min, x_max, y_max = self.calculate_mouth_box(MP_tensor)
            cropped_frame[y_min:y_max,x_min:x_max] = image[y_min:y_max,x_min:x_max]
        else:
            routes_idx=[]
            p1 = [pair[0]for pair in face_oval]
            p2 = [pair[1]for pair in face_oval]
            #init_p1 = p1[0]
            init = p2[0]
            for _ in range(len(face_oval)):
                index = p1.index(init)
                init = p2[index]                
                routes_idx.append((p1[index],p2[index]))

            routes=[]
            for source_idx, target_idx in routes_idx:
                source = face_landmarks[source_idx]
                target = face_landmarks[target_idx]

                relative_source = (int(image.shape[1] * source[0]), int(image.shape[0] * source[1]))
                relative_target = (int(image.shape[1] * target[0]), int(image.shape[0] * target[1]))
                routes.append(relative_source)
                routes.append(relative_target) 

            mask = np.zeros((image.shape[0], image.shape[1]))                          
            mask = cv2.fillConvexPoly(mask,np.array(routes),1)
            mask = mask.astype(bool)
            cropped_frame[mask] = image[mask]

        if gray:
            cropped_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY) 

        if vertical_squeeze > 0:
            b = self.find_bounding_box(cropped_frame)
            x = cropped_frame[b[1]:b[3],b[0]:b[2]]
            h,w = x.shape
            new_edges = np.zeros((h+(2*vertical_squeeze), w))
            new_edges[vertical_squeeze:vertical_squeeze+h] = x
            new_edges = cv2.resize(new_edges,(w,h))
            cropped_frame[b[1]:b[3],b[0]:b[2]] = new_edges
        return cropped_frame 
    
    def grabcut_segmentation(self, image, rect=None, mask=None, iterations=5):
        """
        Function to segment a frame using GrabCut algorithm.
        
        Args:
            image (np.array): Input image/frame to segment.
            rect (tuple): Optional. A rectangle (x, y, width, height) around the foreground.
                        Example: (50, 50, 450, 290)
            mask (np.array): Optional. Binary mask to indicate foreground and background.
            iterations (int): Number of GrabCut iterations. Default is 5.
        
        Returns:
            np.array: Segmented image with background removed (black background).
        """
        # Convert image to a copy
        img = image.copy()

        # Initialize mask if not provided
        if mask is None:
            mask = np.zeros(img.shape[:2], dtype=np.uint8)  # Create an empty mask with 0s
        else:
            mask = np.where(mask == 255, cv2.GC_FGD, cv2.GC_BGD).astype('uint8')

        # Create models for GrabCut
        bgd_model = np.zeros((1, 65), np.float64)  # Background model
        fgd_model = np.zeros((1, 65), np.float64)  # Foreground model

        # If rect is provided, use the rectangle-based GrabCut approach
        if rect is not None:
            cv2.grabCut(img, mask, rect, bgd_model, fgd_model, iterations, cv2.GC_INIT_WITH_RECT)
        else:
            # If a mask is provided, use mask-based GrabCut
            if mask is None:
                raise ValueError("Either 'rect' or 'mask' must be provided.")
            cv2.grabCut(img, mask, None, bgd_model, fgd_model, iterations, cv2.GC_INIT_WITH_MASK)

        # Modify the mask to mark foreground and background pixels
        # Possible mask values: 
        # 0: background, 1: probable background, 2: foreground, 3: probable foreground
        mask_2 = np.where((mask == 2) | (mask == 3), 1, 0).astype('uint8')

        # Apply the mask to get the segmented image
        segmented_image = img * mask_2[:, :, np.newaxis]  # Masking the image

        return segmented_image
    
    def skin_detection(self,frame,signer):  
        space = cv2.cvtColor(frame, cv2.COLOR_RGB2YCrCb)
        if signer =="Marcel":
            lower_skin = np.array([60, 150, 77])   
            upper_skin = np.array([255, 190, 120])  
        elif signer =="Jay":
            lower_skin = np.array([60, 120, 77])   
            upper_skin = np.array([255, 255, 127]) 
            
        elif signer =="Rachel":
            if (abs(frame[:5, :5]-[144,166,89]) < 10).all(): # studi vs in-house
                lower_skin = np.array([145, 131, 103])    
            else:   
                lower_skin = np.array([100, 121, 93])  
            upper_skin = np.array([255, 190, 126])  
        else:
            raise TypeError("Please set the signer into Marcel, Rachel or Jay. Skin_detection function in utils.py")         
        mask = cv2.inRange(space, lower_skin, upper_skin)
        # remove noise        
        # mask = cv2.erode(mask, np.ones((3,3), np.uint8), iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8), iterations=1)
        # mask = cv2.dilate(mask, np.ones((5,5), np.uint8), iterations=1)
        skin = cv2.cvtColor(cv2.bitwise_and(frame, frame, mask=mask), cv2.COLOR_BGR2GRAY)
        return skin 
    
    def get_edge(self,input_img, detector = "Sobel"):
        input_array = torch.clamp((input_img + 1) * 127.5, 0, 255).byte()
        np_img = input_array[0].cpu().numpy()    
        # np_img = cv2.blur(np_img, (5, 5))
        if detector == "Canny":
            edges = cv2.Canny(np_img, 0, 225) 
        else:
            grad_x = cv2.Sobel(np_img, cv2.CV_64F, 1, 0, ksize=1)
            grad_y = cv2.Sobel(np_img, cv2.CV_64F, 0, 1, ksize=1)
            abs_grad_x = cv2.convertScaleAbs(grad_x)
            abs_grad_y = cv2.convertScaleAbs(grad_y)
            edges = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
            
        edge_tensor =  torch.tensor(edges, dtype=torch.float32) / 255.0 * 2.0 - 1.0
        return edge_tensor.unsqueeze(0)
    
    def Rachel_hair_removal(self,face,hand,skin):
        face[face !=0] = 1
        hand[hand !=0] = 1
        mask = hand + face
        mask[mask > 1] = 1                
        mask = cv2.erode(mask[0], np.ones((5,5), np.uint8), iterations=1)
        mask = cv2.dilate(mask, np.ones((5,5), np.uint8), iterations=1)[np.newaxis,...]       
        return mask * skin

    def find_bounding_box(self,image):
        if len(image.shape) ==3:
            image = image.astype(float)[0]
        mini = np.min(image)
        # Find the coordinates of non-zero pixels
        non_zero_pixels = np.argwhere(image > mini)
        
        if non_zero_pixels.size == 0:
            # No non-zero pixels found
            return None

        # Get the minimum and maximum coordinates
        y_min, x_min = np.min(non_zero_pixels, axis=0)
        y_max, x_max = np.max(non_zero_pixels, axis=0)
        
        # Define the bounding box coordinates
        bounding_box = (x_min, y_min, x_max, y_max)        
        return bounding_box
    def calculate_mouth_box(self,MP_tensor, buffer = 5):    
        if MP_tensor is not None:
            mouth_points = MP_tensor[C.MOUTH_LANDMARKS]
            x_coords = [int(point[0].item()) for point in mouth_points]
            y_coords = [int(point[1].item()) for point in mouth_points]

            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            return (x_min- buffer, y_min - buffer, x_max + buffer, y_max + buffer)   
        return None  # If no face is detected
    
    def generate_centres(self,first_center, target_centre, n_points):
        x_centres = np.linspace(first_center[0], target_centre[0], n_points)
        y_centres = np.linspace(first_center[1], target_centre[1], n_points)
        centres = np.column_stack((x_centres, y_centres))  # Efficiently pairs x and y  
        centres = np.round(centres).astype(int)      
        return centres
    
    def shift_mask_to_new_center(self, m, new_center):
        box = self.find_bounding_box(m[0])        #xmin, ymin, xmax, ymax 
        current_center = (box[0] + (box[2]-box[0]) // 2, box[1] + (box[3]-box[1]) // 2)  # horizontal, vertical
        translation = (new_center[0] - current_center[0], new_center[1] - current_center[1])        
        shifted_mask = shift(m[0].astype(float), shift=translation, mode='constant', cval=0)        
        shifted_mask[shifted_mask < 0.01] = 0 
        shifted_mask = np.expand_dims(shifted_mask, axis=0)   
        shift_hand = self.find_bounding_box(shifted_mask[0])

        roi = shifted_mask[0][shift_hand[1]:shift_hand[3],shift_hand[0]:shift_hand[0]+40]
        roi_2 = shifted_mask[0][shift_hand[1]:shift_hand[3],shift_hand[2]-40:shift_hand[2]]
        row_sums = np.sum(roi,axis=1)
        row_sums[row_sums < 10] = 0
        non_zero_indices = np.nonzero(row_sums)[0]
        new_value1 = shift_hand[1] + non_zero_indices[-1]  # ((non_zero_indices[0] + non_zero_indices[-1]) / 2)

        
        row_sums = np.sum(roi_2,axis=1)
        row_sums[row_sums < 10] = 0
        non_zero_indices = np.nonzero(row_sums)[0]
        new_value2 = shift_hand[1] + non_zero_indices[-1]  #((non_zero_indices[0] + non_zero_indices[-1]) / 2)

        shift_hand = (shift_hand[0], new_value1, shift_hand[2], new_value2)
        return shifted_mask, shift_hand
    
    def crop_hand_gray_normalised(self,args, MP_tensor, frame, frame_no, hand,face_mask,new_hand_centre):
        translation = (0, 0, 0, 0)
        if args.opt.hand_crop:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            hand = (gray*hand).astype('uint8')[0] /255
            hand_mask = np.expand_dims(hand,axis=0)

            if args.change_hand_position:
                hand_mask, translation = self.shift_mask_to_new_center(hand_mask, new_hand_centre)
            if args.opt.hand_edge:
                hand = np.array(self.get_edge(torch.from_numpy(hand_mask),detector = args.opt.edge_detector))                      
                    
        if args.opt.face_crop:
            face = self.get_face_crop(MP_tensor, frame,face_mask, mouth_box = args.opt.mouth_box)/255 
            # face[face>0] = 1
            # face = cv2.bitwise_and(frame, frame, mask=face.astype(np.uint8))
            face_mask = np.expand_dims(face,axis=0)       
            if args.opt.face_edge:
                face = np.array(self.get_edge(torch.from_numpy(face_mask),detector = args.opt.edge_detector))
        
        if args.opt.skin_crop:
            skin = self.skin_detection(frame,args.opt.signer) /255  #(SAM_face or SAM_hand)
            skin_mask = np.expand_dims(skin,axis=0)
            if args.opt.skin_edge:
                skin = np.array(self.get_edge(torch.from_numpy(skin_mask),detector = args.opt.edge_detector))           
                
        # if SAM_hand and SAM_face and SAM_skin:
        if args.opt.signer == "Rachel" and args.opt.hand_crop and args.opt.face_crop and args.opt.skin_crop and not args.opt.mouth_box:
            if os.path.exists(args.saving_file_path):
                face_mask_zeros = np.zeros_like(face_mask)
                skin = self.Rachel_hair_removal(face_mask_zeros,hand_mask,skin_mask)
                skin = np.array(self.get_edge(torch.from_numpy(skin),detector = args.opt.edge_detector))  
                # Load the NumPy file
                data = np.load(args.saving_file_path)
                if frame_no < len(data):
                    mask_zeros = np.full_like(skin, -1)
                    # TODO compute these numbers (mouth box) automatically
                    mask_zeros[:,160:430,400:630] = data[frame_no]/3
                    # mask_zeros = mask_zeros + skin
                    skin = np.where(skin > -1, skin, mask_zeros)  
            else:
                skin = self.Rachel_hair_removal(face_mask,hand_mask,skin_mask)
                skin = np.array(self.get_edge(torch.from_numpy(skin),detector = args.opt.edge_detector))


            # centre = TM(frame, cv2.imread("/home/basheer/Signapse/new/signapse/inputs/eyes.png"))
            # buffer = 40
            # if abs(centre[0] - 505) > buffer or abs(centre[1] - 234) > buffer:
            #     centre = [505, 234]
            # img_np = np.load("/home/basheer/Signapse/new/signapse/inputs/eyes.npy")
            # h ,w = img_np.shape
            # skin[0,   int(centre[1] - (h/2)) : int(centre[1] + (h/2)) , int(centre[0] - (w/2)) : int(centre[0] + (w/2))  ] = img_np
            # skin[0,220:245,440:574] = np.load("/home/basheer/Signapse/new/signapse/inputs/eyes.npy")
            return skin, translation
            
        if args.opt.hand_crop and args.opt.face_crop:
            return (np.concatenate((hand, face))), translation
        elif args.opt.skin_crop:
            return skin  , translation
        elif args.opt.hand_crop:
            return hand, translation
        elif args.opt.face_crop:
            return face , translation
        else:    
            raise TypeError("Please set the correct flags for SAM hand and face masks")
    
    def adjust_wrists(self,  left_hand, right_hand, translation): #x, y, w, h 
        x_min, y_min, x_max, y_max = translation
        right_hand  = torch.Tensor((x_min,y_min)).to(device=left_hand.device)
        left_hand = torch.Tensor((x_max,y_max)).to(device=right_hand.device)
        return left_hand, right_hand
    
    def get_heatmaps_crops(self,input_frame,MP_results_gen,GAN_model, args,iii=0, hand_mask=None,face_mask=None,new_hand_centre=(0,0)):
        resolution = args.opt.loadSize
        MP_results_gen = MP_results_gen*resolution 
        if args.opt.sam: # do sam
            cropped_hand, translation = self.crop_hand_gray_normalised(args, MP_results_gen,input_frame, iii,hand_mask,face_mask,new_hand_centre)
            if args.change_hand_position:
                MP_results_gen[6], MP_results_gen[27] = self.adjust_wrists(MP_results_gen[6], MP_results_gen[27], translation)
                # MP_results_gen[6], MP_results_gen[27] = self.adjust_wrists(copy.copy(cropped_hand[0]), MP_results_gen[6], MP_results_gen[27])

        # First, create a HeatMap representation from the MediaPipe tensor
        results_pose = MP_results_gen[:6]
        results_LH = MP_results_gen[6:27]
        results_RH = MP_results_gen[27:48]
        results_face = MP_results_gen[48:176]
        results_hip = MP_results_gen[176:]

        face_connections = C.FACE_CONNECTIONS_SAM
        heat_map_dim = 5 + 40 + len(face_connections) + 3
        heat_map = np.zeros((heat_map_dim, resolution, resolution), np.uint8)
        

        # MP Body
        draw_line_nonan(heat_map[0], (results_pose[0]), (results_pose[1]), c=(1, 1, 1), t=1, width=1)
        # Left
        draw_line_nonan(heat_map[1], (results_pose[0]), (results_pose[2]), c=(1, 1, 1), t=1, width=1)
        # draw_line_nonan(heat_map[2], (results_pose[2]), (results_pose[4]), c=(1, 1, 1), t=1, width=1)
        draw_line_nonan(heat_map[2], (results_pose[2]), (results_LH[0]), c=(1, 1, 1), t=1, width=1)
        # Right
        draw_line_nonan(heat_map[3], (results_pose[1]), (results_pose[3]), c=(1, 1, 1), t=1, width=1)
        # draw_line_nonan(heat_map[4], (results_pose[3]), (results_pose[5]), c=(1, 1, 1), t=1, width=1)
        draw_line_nonan(heat_map[4], (results_pose[3]), (results_RH[0]), c=(1, 1, 1), t=1, width=1)

        # MP Hands
        for i in range(5):
            draw_line_nonan(heat_map[4 + 4 * i + 1], (results_LH[0]), (results_LH[i * 4 + 1]), c=(1, 1, 1), t=1, width=1)
            draw_line_nonan(heat_map[4 + 4 * i + 2], (results_LH[i * 4 + 1]), (results_LH[i * 4 + 2]), c=(1, 1, 1), t=1, width=1)
            draw_line_nonan(heat_map[4 + 4 * i + 3], (results_LH[i * 4 + 2]), (results_LH[i * 4 + 3]), c=(1, 1, 1), t=1, width=1)
            draw_line_nonan(heat_map[4 + 4 * i + 4], (results_LH[i * 4 + 3]), (results_LH[i * 4 + 4]), c=(1, 1, 1), t=1, width=1)

        for i in range(5):
            draw_line_nonan(heat_map[24 + 4 * i + 1], (results_RH[0]), (results_RH[i * 4 + 1]), c=(1, 1, 1), t=1, width=1)
            draw_line_nonan(heat_map[24 + 4 * i + 2], (results_RH[i * 4 + 1]), (results_RH[i * 4 + 2]), c=(1, 1, 1), t=1, width=1)
            draw_line_nonan(heat_map[24 + 4 * i + 3], (results_RH[i * 4 + 2]), (results_RH[i * 4 + 3]), c=(1, 1, 1), t=1, width=1)
            draw_line_nonan(heat_map[24 + 4 * i + 4], (results_RH[i * 4 + 3]), (results_RH[i * 4 + 4]), c=(1, 1, 1), t=1, width=1)

        ## FACE
        for c, connection in enumerate(face_connections):
            new_connection = (GAN_model.face_points[connection[0]], GAN_model.face_points[connection[1]])
            draw_line_nonan(heat_map[45 + c], (results_face[new_connection[0]]), (results_face[new_connection[1]]), c=(1, 1, 1), t=1, width=1)

        # MP Hip
        draw_line(heat_map[169], results_hip[0],  results_hip[1], c=(1, 1, 1), t=1, width=1)
        draw_line(heat_map[170], results_hip[0], results_pose[0], c=(1, 1, 1), t=1, width=1)
        draw_line(heat_map[171], results_hip[1], results_pose[1],  c=(1, 1, 1), t=1, width=1)      
        
 
        if not torch.is_tensor(heat_map):
            heat_map = torch.tensor(heat_map)
            
        heat_map_2 = copy.copy(heat_map)    
        # set poses       
        heat_map =[]
        if not args.opt.remove_body_pose:
            heat_map.append(heat_map_2[:5])    
                
        if not args.opt.remove_hand_pose:
            heat_map.append(heat_map_2[5:45]) 
            
        if not args.opt.remove_face_pose:
            heat_map.append(heat_map_2[45:169])
                                
        if not args.opt.remove_hip_pose:
            heat_map.append(heat_map_2[169:172])
                        
        heat_map = np.concatenate(heat_map, axis=0)

        # face_mesh
        if args.opt.face_mesh:
            heat_map = np.concatenate((heat_map, heat_map_2[-1:]), axis=0) 

        if args.opt.sam:               
            # Normalisation
            if args.opt.crop_normalise:
                handcrop_transform = transforms.Compose([transforms.Normalize((0.5,), (0.5,))])
                if args.opt.hand_crop and args.opt.face_crop and args.opt.skin_crop:
                    cropped_hand[0] = np.array(handcrop_transform(torch.from_numpy(cropped_hand[0].astype('float16')).unsqueeze(dim=0)))
                elif args.opt.hand_crop and args.opt.face_crop:
                    cropped_hand[1] = np.array(handcrop_transform(torch.from_numpy(cropped_hand[1].astype('float16')).unsqueeze(dim=0)))
                    cropped_hand[0] = np.array(handcrop_transform(torch.from_numpy(cropped_hand[0].astype('float16')).unsqueeze(dim=0)))
                elif args.opt.hand_crop:
                    cropped_hand[0] = np.array(handcrop_transform(torch.from_numpy(cropped_hand[0].astype('float16')).unsqueeze(dim=0)))
                elif args.opt.face_crop : #and not opt.signer =="Rachel"
                    cropped_hand[1] = np.array(handcrop_transform(torch.from_numpy(cropped_hand[1].astype('float16')).unsqueeze(dim=0)))
                else:
                    cropped_hand[0] = np.array(handcrop_transform(torch.from_numpy(cropped_hand[0].astype('float16')).unsqueeze(dim=0)))
            if not torch.is_tensor(cropped_hand):
                cropped_hand = torch.tensor(cropped_hand)
        else:
            cropped_hand = None

        # After you've created heatmap label, Concetenate the base image tensor on to the front
        if not torch.is_tensor(heat_map):
            heat_map = torch.tensor(heat_map)  
                    
        
        if args.opt.remove_mouth_pose:
            mouth_heatmaps_index = [5, 7, 11, 14, 17, 20, 24, 25, 27, 28, 32, 33, 34, 35, 38, 39, 41, 45, 47, 51, 60, 61, 65, 66, 74, 76, 78, 87, 91, 95, 98, 100, 102, 103, 106, 111, 116, 119, 124, 125]
            face_without_mouth_heatmaps_index = [m for m in range(len(heat_map)) if m not in mouth_heatmaps_index]
            heat_map = heat_map[face_without_mouth_heatmaps_index]

        if args.opt.sam: 
            # mask the heatmaps
            heat_map[5:-3] = self.mask_heatmaps(heat_map[5:-3],copy.deepcopy(cropped_hand)) 
      
        return heat_map,cropped_hand
    
    def mask_heatmaps(self,heat_map,crops):
        # add the channels
        mask = torch.sum(crops, dim=0)
        # get the background value
        background_value = torch.mean(mask[:10,:10])
        # change to 1 and 0 where the background is 1 and the objects are 0, and fill holes   
        mask = (mask > background_value).float()        
        # Convert mask to binary and fill holes (stays in NumPy here)
        mask_np = mask.cpu().numpy()  # Convert to NumPy if using binary_fill_holes
        mask_np = binary_fill_holes(mask_np).astype(float)
        mask = torch.tensor(mask_np).to(heat_map.device) 
        mask = 1 - mask
        return  heat_map * mask   # mask only the face. Ignore the hands, hip and the main body


    
    # Convert a heatmap representation to an image
    def convert_limb_heatmap(self,heat_map,imtype=np.uint8):
        heat_map = np.array(heat_map)
        full_heatmap = np.zeros((heat_map.shape[1], heat_map.shape[2]), imtype)
        for frame in heat_map:
            full_heatmap = np.add(full_heatmap,frame)  #full_heatmap + frame
        full_heatmap = ((full_heatmap != 0) == False)*255
        return full_heatmap.astype(imtype)
    
    
    def get_pose_image(self,opt,input_frame,generated,heat_map,crops):
        if opt.sam:            
            if opt.multi_frames:
                total_maps_per_sample = (len(heat_map)//((opt.num_frames*2)+1)) - len(crops[0])
                input_label = self.convert_limb_heatmap(heat_map[opt.num_frames*total_maps_per_sample:(opt.num_frames+1)*total_maps_per_sample,:,:]).reshape((heat_map.shape[1], heat_map.shape[2], 1))
            
            else:
                input_label = self.convert_limb_heatmap(heat_map[:-crops[0].shape[0]]).reshape((heat_map.shape[1], heat_map.shape[2], 1))            

            if  opt.crop_normalise:
                if opt.erusion:
                    avg_bg = -int(crops[0][0][:10,:10].mean()) # to keep the background zeros
                    hand = (crops[0][0].numpy() + avg_bg ) * 255
                    if not opt.merge_crops:
                        avg_bg = -int(crops[0][1][:10,:10].mean())
                        body = (crops[0][1].numpy() + avg_bg ) * 255
                else:
                    avg_bg = -int(crops[0][0][:10,:10].mean())
                    hand = (crops[0][0].numpy()+ avg_bg) * 255
                    if crops[0].shape[0] > 1:
                        avg_bg = -int(crops[0][1][:10,:10].mean())
                        body = (crops[0][1].numpy()+ avg_bg) * 255
                        body[body==0]=255
                hand[hand==0]=255             
 
                
                if crops[0].shape[0] > 1:  #(opt.hand_crop and opt.face_crop) and not (opt.skin_crop or opt.merge_crops):
                    input_label[:,:,0] = (input_label[:,:,0]) + (255 - (hand).astype(np.uint8))  + (255-(body).astype(np.uint8)) 
                else:
                    input_label[:,:,0] = (255* ((input_label[:,:,0])/255 *  (hand).astype(np.uint8)/255)) #(255 - (hand).astype(np.uint8)) 
                             
                    
            else: 
                if (opt.hand_crop and opt.face_crop) and not (opt.skin_crop or opt.merge_crops):                              
                    input_label[:,:,0] = input_label[:,:,0] + (heat_map[-2]*255).numpy().astype(np.uint8) + (heat_map[-1]*255).numpy().astype(np.uint8)
                else:
                    input_label[:,:,0] = input_label[:,:,0] + (heat_map[-1]*255).numpy().astype(np.uint8)
                    
                
        elif opt.hand_crop or opt.face_crop or opt.skin_crop:
            if opt.N2N:
                input_label = self.convert_limb_heatmap(heat_map).reshape((heat_map.shape[1], heat_map.shape[2], 1))
            elif opt.multi_frames:
                total_maps_per_sample = (len(heat_map)//((opt.num_frames*2)+1)) - len(crops[0])
                input_label = self.convert_limb_heatmap(heat_map[opt.num_frames*total_maps_per_sample:(opt.num_frames+1)*total_maps_per_sample,:,:]).reshape((heat_map.shape[1], heat_map.shape[2], 1))
            else:
                input_label = self.convert_limb_heatmap(heat_map[:-1]).reshape((heat_map.shape[1], heat_map.shape[2], 1))
            if opt.crop_normalise:
                if opt.hand_crop or opt.skin_crop:
                    hand = (crops[0].numpy() +1 ) * 255               
                    hand[hand==0]=255                    
                    input_label[:,:,0] = input_label[:,:,0] + (255 - (hand).astype(np.uint8))
                else :
                    if opt.erusion:
                        body = (crops[1].numpy() +1 ) * 255
                    else:
                        body = crops[1].numpy() * 255                    
                    body[body==0]=255
                    input_label[:,:,0] = input_label[:,:,0] + (255-(body).astype(np.uint8)) 
            else:            
                input_label[:,:,0] = input_label[:,:,0] + (heat_map[-1]*255).numpy().astype(np.uint8)          

        else:                    
            input_label = self.convert_limb_heatmap(heat_map).reshape((heat_map.shape[1], heat_map.shape[2], 1))
                
        input_label = np.concatenate((input_label, input_label, input_label), axis=2)
        pose_image = np.ascontiguousarray(input_label)[:, :opt.loadSize]
        pose_image = cv2.cvtColor(pose_image, cv2.COLOR_BGR2RGB)
        input_frame = cv2.resize(input_frame, dsize=(opt.loadSize, opt.loadSize),
                                    interpolation=cv2.INTER_CUBIC)
        output_frame = np.concatenate((input_frame, pose_image, generated), axis=1)

        return output_frame

    def generate_GAN_frame_maps_crops(self,input_frame,maps,crops,GAN_model,opt,detailed_video=False):    
        if crops[0] == None:
            heat_map = np.concatenate(maps, axis=0)  
        else:
            heat_map = np.concatenate((np.concatenate(maps, axis=0), np.concatenate(crops, axis=0)), axis=0)  
               
        # After you've created heatmap label, Concetenate the base image tensor on to the front
        if not torch.is_tensor(heat_map):
            heat_map = torch.tensor(heat_map)
            
        if GAN_model.opt.base_style:
            torch_label = torch.cat((GAN_model.base_tensor, heat_map.float().unsqueeze(0)), dim=1).unsqueeze(0)
        else:
            torch_label = heat_map.float().unsqueeze(0).unsqueeze(0)
        # After you've created the full heatmap label, pass it through to the GAN model
        with torch.no_grad():
            gen = GAN_model.forward(Variable(torch_label),face=None)
            if len(gen) > 3:
                output_frame = []
                n = int((len(gen)/3) / 2)
                generated = gen[3*n:3*(n+1)]
                generated = np.ascontiguousarray(tensor2im(generated))
                if detailed_video:  
                    output_frame = self.get_pose_image(opt,input_frame,generated,maps[n],crops[n])  
                else:
                    output_frame = generated 
                
            else:
                generated = np.ascontiguousarray(tensor2im(gen))
                if detailed_video:      
                    output_frame = self.get_pose_image(opt,input_frame,generated,heat_map,crops)  
                else:
                    output_frame = generated       
        return output_frame     
    
