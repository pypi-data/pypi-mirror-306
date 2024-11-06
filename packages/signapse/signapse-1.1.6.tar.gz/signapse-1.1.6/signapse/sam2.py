import os
import cv2
import imageio
import shutil
import torch
import numpy as np
import subprocess
from pathlib import Path
import matplotlib.pyplot as plt
import mediapipe as mp
mp_holistic = mp.solutions.holistic


from scipy.signal import find_peaks
# from signapse.heatmaps import HEATMAPS
from signapse.poses import POSE
from sam2.build_sam import build_sam2_video_predictor

def find_top_image_differences(images, num_peaks=5, threshold_peak = 500, peak_height_threshold=3000):
    """
    Identify the top N differences between consecutive images based on the peak of absolute differences.

    Parameters:
    images (list of np.array): List of images in NumPy array format.
    num_peaks (int): Number of top peaks to find. Defaults to 5.
    peak_height_threshold (int or float): Minimum height of peaks to consider. Defaults to 6000.

    Returns:
    list: Indices of the top N peaks sorted in ascending order.
    """
    # Validate inputs
    if not images or len(images) < 2:
        raise ValueError("The input 'images' should be a list containing at least two images.")
    if num_peaks <= 0:
        raise ValueError("The number of peaks 'num_peaks' should be greater than zero.")
    
    # Compute absolute differences between consecutive images
    subtracted_images = [
        abs(np.sum(images[i].squeeze()) - np.sum(images[i - 1].squeeze()))
        for i in range(1, len(images))
    ]
    result = np.array(subtracted_images)
    # Find peaks above the specified height
    peaks, _ = find_peaks(result, threshold=threshold_peak) #height=peak_height_threshold    
    if len(peaks) == 0:
        return []  # No peaks found    
    # Sort peaks by their prominence (absolute difference value) in descending order
    sorted_indices = np.argsort(result[peaks])[::-1]
    top_peaks = peaks[sorted_indices[:num_peaks]]    
    # Return indices of the top peaks, sorted in ascending order for clarity
    return sorted(top_peaks + 1)  # Correct indexing for returned peak positions

def bounding_box_and_center(points):
    # points = np.array(points[points != 0])
    points_np = points.numpy()
    points_2 = points_np[(points_np != 0).all(axis=1)]
    # Find the minimum and maximum values for x and y
    min_x, min_y = np.min(points_2, axis=0)
    max_x, max_y = np.max(points_2, axis=0)
    # Calculate the center point
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    # Define the bounding box
    bbox = (int(min_x), int(min_y), int(max_x), int(max_y))
    # Define the center point
    center = ((int(center_x), int(center_y)))

    return bbox, center


    #     return [left_wrist_coords, right_wrist_coords, face_center_coords]
    # else:
    #     return [None, None, None]
    # vertical_shift = 600
    # f = frame[vertical_shift:,:,0]
    # f[f>0] = 1
    # rows = np.any(f == 1, axis=1)
    # cols = np.any(f == 1, axis=0)

    # # Determine the boundaries of the bounding box
    # y_min = vertical_shift + np.argmax(rows)        # First row with a 1
    # y_max = vertical_shift + (len(rows) - np.argmax(rows[::-1]) - 1)  # Last row with a 1
    # x_min = np.argmax(cols)           # First column with a 1
    # x_max = len(cols) - np.argmax(cols[::-1]) - 1 
    # return None,[x_min, y_min, x_max, y_max]


    
def save_masks( no_frame_names, video_segments, vis_frame_stride=1):
    mask=[]
    for out_frame_idx in range(0, no_frame_names, vis_frame_stride):       
    # for out_frame_idx in sorted(video_segments.keys()):    
        if out_frame_idx in video_segments.keys():
            for _, out_mask in video_segments[out_frame_idx].items():
                mask.append(out_mask)

    return mask

class SAM2Initializer:
    def __init__(self, checkpoint_path, model_config_path):
        self.checkpoint_path = checkpoint_path
        self.model_config_path = model_config_path

        # Ensure we're using bfloat16 precision for the entire notebook
        self.autocast = torch.autocast(device_type="cuda", dtype=torch.bfloat16)
        self.autocast.__enter__()

        # Check for GPU compatibility
        if torch.cuda.is_available() and torch.cuda.get_device_properties(0).major >= 8:
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True

        # Build the SAM 2 predictor
        self.predictor = self._initialize_predictor()

    def _initialize_predictor(self):
        """Initialize the SAM 2 video predictor."""
        return build_sam2_video_predictor(self.model_config_path, self.checkpoint_path)

    def get_predictor(self):
        """Return the initialized predictor."""
        return self.predictor

    # def process_frame(self, input_dir):
    #     if isinstance(input_dir, np.ndarray):
    #         skin_mask =  HEATMAPS().skin_detection(cv2.cvtColor(input_dir, cv2.COLOR_BGR2RGB),'Rachel',include_hair = False) 
    #         skin_mask[skin_mask> 0] = 1
    #         # masked_image = input_dir * skin_mask[:, :, np.newaxis]
    #         return skin_mask

        # elif isinstance(input_dir, str):
        #     if os.path.isfile(input_dir):
        #         for filename in os.listdir(input_dir):
        #             # Create the full file path
        #             input_path = os.path.join(input_dir, filename)
        #             frame =  cv2.imread(input_path)
        #             skin_mask =  HEATMAPS().skin_detection(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),'Rachel',include_hair = False) 
        #             skin_mask[skin_mask> 0] = 1
        #             masked_image = frame * skin_mask[:, :, np.newaxis]
        #             output_path = os.path.join(input_dir, filename)
        #             cv2.imwrite(output_path, masked_image)


    def extract_frames(self, video_path, image_dir, ending_frame = None):
        reader = imageio.get_reader(video_path)
        fps = reader.get_meta_data().get('fps', None)
        reader.close()
        if fps is not None:
            if fps == 0:
                raise ValueError("FPS is 0, which is invalid")
        else:
            raise ValueError("FPS not found in video metadata")
        
        if Path(image_dir).exists() and Path(image_dir).is_dir():
            shutil.rmtree(Path(image_dir))
    
        Path(image_dir).mkdir(parents=True, exist_ok=True)
        output_pattern = Path(image_dir) / '%05d.jpg'

        ffmpeg_command = [
            'ffmpeg',
            '-i', video_path,
            '-q:v', '2',
            '-start_number', '0',
            '-pix_fmt', 'yuvj420p'
            # str(output_pattern)
        ]
        if ending_frame > 0:
            ffmpeg_command.extend(['-frames:v', str(ending_frame)])
        ffmpeg_command.extend([str(output_pattern)])

        try:
            subprocess.run(ffmpeg_command, check=True)
            print(f"Frames extracted and saved to: {image_dir}")
            return fps
        except subprocess.CalledProcessError as e:
            shutil.rmtree(image_dir)  # Clean up if error occurs
            raise ValueError(f"An error occurred while extracting frames: {e}")
        
    def add_points(self, frame_mask, boxes, points, labels, ann_frame_idx, ann_obj_id, predictor, inference_state):
        if points is not None:
            points = np.array(points, dtype=np.float32)
        if labels is not None:
            labels = np.array(labels, np.int32)
        if boxes is not None:
            boxes = np.array(boxes, dtype=np.float32)

        if frame_mask is not None:
            _, _, _ = predictor.add_new_mask(
                inference_state,
                frame_idx=ann_frame_idx,
                obj_id=ann_obj_id,
                mask = frame_mask,
                )

        _, _, _ = predictor.add_new_points_or_box(  #.add_new_points_or_box(   this function has been added after the release in one week
            inference_state=inference_state,
            frame_idx=ann_frame_idx,
            obj_id=ann_obj_id,
            box = boxes,
            points=points,
            labels=labels,
        )
        return predictor
    
    def add_point_to_the_predictor(self,NUM_Frame, sam2_initializer, inference_state, tmp_image_dir, predictor):
        if isinstance(NUM_Frame, int):
            first_frame = cv2.imread(os.path.join(tmp_image_dir,f'{NUM_Frame:05d}.jpg'))
            labels, points, boxes, frame_mask = self.get_wrist_points(first_frame)
            if labels is not None:
                ann_obj_id = 1
                predictor = sam2_initializer.add_points(frame_mask, boxes,points,labels, NUM_Frame, ann_obj_id, predictor, inference_state)
        elif isinstance(NUM_Frame, list):
            for num in NUM_Frame:
                first_frame = cv2.imread(os.path.join(tmp_image_dir,f'{num:05d}.jpg'))
                labels, points, boxes, frame_mask = self.get_wrist_points(first_frame)
                if labels is not None:
                    ann_obj_id = 1
                    predictor = sam2_initializer.add_points(frame_mask, boxes,points,labels, num, ann_obj_id, predictor, inference_state)
        return predictor
    
    def predict(self,predictor, inference_state):
        video_segments = {}
        for out_frame_idx, out_obj_ids, out_mask_logits in predictor.propagate_in_video(inference_state):
            video_segments[out_frame_idx] = {
                out_obj_id: (out_mask_logits[i] > 0.0).cpu().numpy()
                for i, out_obj_id in enumerate(out_obj_ids)
            }
        return video_segments
    
    def get_wrist_points(self,frame):    
        height, width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        with mp_holistic.Holistic(static_image_mode=False,model_complexity=2,min_detection_confidence=0.0,min_tracking_confidence=0.0) as holistic:
            MP_tenor = POSE(width).results_to_small_tensor(holistic.process(rgb_frame),None)
            if torch.eq(MP_tenor, 0.0).all().item():
                MP_tenor = POSE(width).results_to_small_tensor(holistic.process(frame),None)

        if (torch.eq(MP_tenor[6:27], 0.0).any().item() and torch.eq(MP_tenor[27:48], 0.0).any().item()) or torch.eq(MP_tenor[48:-2], 0.0).any().item():
            print('No hand is detected')
            return None,None,None,None
        elif torch.eq(MP_tenor[6:27], 0.0).any().item():
            MP_tenor[6:27] = MP_tenor[27:48]

        elif torch.eq(MP_tenor[27:48], 0.0).any().item():
            MP_tenor[27:48] = MP_tenor[6:27]

        MP_tenor[:,0] = MP_tenor[:,0] * width
        MP_tenor[:,1] = MP_tenor[:,1] * height
        # left_ wrist
        lw = tuple(int(x) for x in MP_tenor[4,:]) 
        rw = tuple(int(x) for x in MP_tenor[5,:])    

        # left hand
        if len(MP_tenor[6:27]) == 0:
            print("The array is empty.")
        else:
            bbox_l, center_l = bounding_box_and_center(MP_tenor[6:27])        
        # right hand
        if len(MP_tenor[27:48]) == 0:
            print("The array is empty.")
        else:
            bbox_r, center_r = bounding_box_and_center(MP_tenor[27:48])
        # face
        if len(MP_tenor[48:-2]) == 0:
            print("The array is empty.")
        else:
            bbox_f, center_f = bounding_box_and_center(MP_tenor[48:-2])

        labels, points =[],[]
        # boxes.append(bbox_l)
        # boxes.append(bbox_r)
        boxes = None
        frame_mask = None #self.process_frame(frame)
        points.append(lw);labels.append(1)
        points.append(rw);labels.append(1)
        points.append(center_l);labels.append(1)
        points.append(center_r);labels.append(1)
        points.append(center_f);labels.append(0)
        return labels, points, boxes, frame_mask
    
    
def get_masks_sam2(input_video, num_correction ,stop, tmp_dir = "./inputs/tmp"):
    model_cfg ="sam2_hiera_l.yaml"
    sam2_checkpoint ="./inputs/sam2_hiera_large.pt"    #fine_tuned_sam2_larger_latest.pt   #sam2_hiera_large.pt
    base_name = os.path.basename(input_video)
    filename, _ = os.path.splitext(base_name)
    tmp_image_dir = os.path.join(tmp_dir, filename)
    print(f'Get images from video.')
    sam2_initializer = SAM2Initializer(sam2_checkpoint, model_cfg)
    predictor = sam2_initializer.get_predictor()
    sam2_initializer.extract_frames(input_video, tmp_image_dir , ending_frame = stop)
    # sam2_initializer.process_frame(tmp_image_dir)
    frame_names = [p for p in os.listdir(tmp_image_dir) if os.path.splitext(p)[-1] in [".jpg", ".jpeg", ".JPG", ".JPEG"]]
    frame_names.sort(key=lambda p: int(os.path.splitext(p)[0]))
    inference_state = predictor.init_state(video_path=tmp_image_dir)
    predictor.reset_state(inference_state)

    top_image_differences = [0] # initialise
    NUM_Frame = [-1]  # initialise
    counter = 0
    print(f'Correction based on the generated masks.')
    while len(top_image_differences) > 0  and counter < 3 :  # No more than a certain times for corrections.
        if NUM_Frame[0] >= top_image_differences[0]: ## break if earlier frame failed 
            print(f'Stop correction because previous frame {top_image_differences[0]} failed.')
            break
        if num_correction > 0  and counter == 0:
            NUM_Frame = np.linspace(0, len(frame_names)-1, num_correction, dtype=int).tolist()
        else:
            NUM_Frame = sorted(list(set(top_image_differences) - set(NUM_Frame))) 
        print(f'Correction attempt No {counter}. Frames no: {NUM_Frame}')
        predictor = sam2_initializer.add_point_to_the_predictor(NUM_Frame, sam2_initializer, inference_state, tmp_image_dir, predictor)
        video_segments = sam2_initializer.predict(predictor, inference_state)
        masks = save_masks(len(frame_names), video_segments)        
        top_image_differences = find_top_image_differences(masks)
        counter += 1

    shutil.rmtree(tmp_image_dir)
    result=[]
    k = 0
    for i in range(len(masks) - 1):
        result.append(np.sum(np.logical_and(masks[i][0]== True , masks[i + 1][0]== False)))
    if result[0] > result[1]:
        result = np.insert(result, 0, 0)
        k = 1
    if result[-1] > result[-2]:
        result = np.append(result, len(result) - 1)
    peaks, _ = find_peaks(result, prominence=15000)
    for i in peaks:
        if i ==1:
            masks[i-k] = masks[i+1-k]
        else:
            masks[i-k] = masks[i-1-k]
    return masks