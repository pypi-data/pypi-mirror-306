import  torch,logging,imageio, os,gzip
import pickle as pickle
import mediapipe as mp
import numpy as np
from PIL import Image, ImageEnhance
logging.basicConfig(level=logging.INFO)

import signapse.constants as C
from signapse.create import GENERATOR
from signapse.mp_utils import INTERPLATION, IMAGE_PROCESSING
from signapse.sam2 import get_masks_sam2

def save_zipped_pickle(obj, filename, protocol=-1):
    with gzip.open(filename, 'wb') as f:
        pickle.dump(obj, f, protocol)

def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = pickle.load(f)
        return loaded_object
    
mp_face_mesh = mp.solutions.face_mesh
face_mesh =  mp_face_mesh.FaceMesh(max_num_faces=1,
                                    static_image_mode=True,
                                    refine_landmarks=True,
                                    min_detection_confidence=0.8,
                                    min_tracking_confidence=0.8)
face_oval = list(mp_face_mesh.FACEMESH_FACE_OVAL)
face_mesh_mop = [num-176 for num in C.FACE_MESH_MOP]

class SAM_CROPS():
    def __init__(self, args):
        super(SAM_CROPS,self).__init__()
        self.args=args  

    def insert_numbers(self, a, b, n):
        n = n-2 # it will take the last and first point in consideration
        if n <= 0:
            return []
        numbers = np.linspace(a, b, num=n+2)#[1:-1]  # Exclude a and b
        numbers = [int(round(num)) for num in numbers]        
        return numbers
    
    def get_face_landmarks(self,image):
        image.flags.writeable = False
        results = face_mesh.process(image)
        image.flags.writeable = True    
        if results.multi_face_landmarks:
            data = results.multi_face_landmarks[0] 
            face_landmarks = np.array([[landmark.x, landmark.y] for landmark in data.landmark])
        else:
            face_landmarks = np.zeros((478,2))
        return face_landmarks
    
    def face_mask(self,img_centre,args):
        mask2=[]
        GENERATOR(args).mkdir_safe("./inputs/Face_files")       
        reader = imageio.get_reader(args.input_video_path)
        for i, frame in enumerate(reader): 
            if i < args.start:
                continue     
            # if i% 50==0:
            #     logging.info("Frame: {}".format(i))
            if args.stop != -1 and i >= args.stop:
                break        
            frame = IMAGE_PROCESSING().apply_norm(frame,img_centre,args.opt.loadSize)             
            face_mask = self.get_face_landmarks(frame)    
            mask2.append(face_mask)
    
        if args.opt.smooth_face_crop:
            mask2 = INTERPLATION().interpolate_All_MP_Tensors(torch.from_numpy(np.array(mask2)),no_zero_start=False)
            Points = mask2[0,48:]  # compute the point distance based on frame 0
            mask2[:,face_mesh_mop] = IMAGE_PROCESSING().mouth_centering(mask2[:,face_mesh_mop], sigma=9)
            # Using the center points of the mouth [13,:] as the center of the face
            dist_to_centre = np.linalg.norm(Points - Points[13,:], axis=-1)
            dist_to_centre = dist_to_centre/np.max(dist_to_centre)
            smoothed_signal = np.array([INTERPLATION().smooth_keypoints(mask2[:,i], i, dist_to_centre[i-48]) for i in range(mask2.shape[1])]) #dist_to_centre[i-48]
            mask2 = np.transpose(smoothed_signal, (1, 0, 2))
        return mask2

        

       
    def sam_masks(self,img_centre):
        if (self.args.opt.face_crop) or (self.args.opt.hand_crop):
            if (self.args.opt.hand_crop):
                if self.args.mask_overwrite:
                    mask = get_masks_sam2(self.args.input_video_path, self.args.num_correction, self.args.stop,tmp_dir = "./inputs/tmp")                
                    save_zipped_pickle(mask, f'./inputs/SAM_files/{self.args.sign_request_id}.pkl')
                else:
                    if  not (os.path.isfile(f"./inputs/SAM_files/{self.args.sign_request_id}.pkl")):
                        mask = get_masks_sam2(self.args.input_video_path, self.args.num_correction, self.args.stop,tmp_dir = "./inputs/tmp")                
                        save_zipped_pickle(mask, f'./inputs/SAM_files/{self.args.sign_request_id}.pkl')

            if self.args.opt.face_crop:
                if self.args.mask_overwrite:
                    mask2 = self.face_mask(img_centre,self.args)
                    save_zipped_pickle(mask2, f'./inputs/Face_files/{self.args.sign_request_id}.pkl')
                else:
                    if  not (os.path.isfile(f"./inputs/Face_files/{self.args.sign_request_id}.pkl")):
                        mask2 = self.face_mask(img_centre,self.args)
                        save_zipped_pickle(mask2, f'./inputs/Face_files/{self.args.sign_request_id}.pkl')
            
