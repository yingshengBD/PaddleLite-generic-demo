# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cv2
import numpy as np
from array import array

if __name__ == "__main__":
    src_img_file_path = '../assets/images/dog.jpg'
    res_bin_file_path = '../assets/results/dog.bin'
    res_img_file_path = '../assets/results/dog.jpg'
    score_threshold = 0.5
    # Decode image and resize it to the target size
    src_image = cv2.imread(src_img_file_path)
    # Convert to float and dump to file
    with open(res_bin_file_path, "rb") as f:
        bboxes = np.fromfile(f, np.float32)
        bboxes = bboxes.reshape([-1, 6])
    num = bboxes.shape[0]
    print(num)
    for i in range(num):
        class_id = bboxes[i][0]
        score = bboxes[i][1]
        if score > score_threshold:
            x0 = bboxes[i][2]
            y0 = bboxes[i][3]
            x1 = bboxes[i][4]
            y1 = bboxes[i][5]
            print("[%d] class_id=%f score=%f bbox=[%f,%f,%f,%f]" %
                  (i, class_id, score, x0, y0, x1, y1))
            x0 = max(int(x0 / 416.0 * src_image.shape[1]), 0)
            y0 = max(int(y0 / 416.0 * src_image.shape[0]), 0)
            x1 = min(int(x1 / 416.0 * src_image.shape[1]), src_image.shape[1])
            y1 = min(int(y1 / 416.0 * src_image.shape[0]), src_image.shape[0])
            cv2.rectangle(src_image, (x0, y0), (x1, y1), (0, 255, 0), 4)
    cv2.imwrite(res_img_file_path, src_image)
