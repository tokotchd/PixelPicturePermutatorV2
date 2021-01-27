import numpy as np
import cv2
import argparse
import os
from sklearn.neighbors import NearestNeighbors  # we perform general knn in order to find the nearest image in colorspace
import random

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('base_image', help='The main image you wish to re-create using permuted images')
    parser.add_argument('sub_images_dir', help='The directory of sub-images you wish to permute into the base_image')
    parser.add_argument('--base_image_scale', help='The desired scale applied to base image before replacing the pixels', type=float, default=1)
    parser.add_argument('--sub_images_size', help='The desired size applied to mini-images to before permuting them', type=int, default=8)
    parser.add_argument('--num_nearest_neighbors', help='The number of nearest colorspace neighbors to consider for image permutation', default=1, type=int)
    args = parser.parse_args()

    # args verification
    base_scaling = args.base_image_scale
    sub_size = args.sub_images_size
    num_nearest_neighbors = args.num_nearest_neighbors

    # load the base image
    base_image = cv2.imread(args.base_image).astype(np.float32)
    h, w, = [int(i * base_scaling) for i in base_image.shape[0:2]]
    base_image = cv2.resize(base_image, dsize=(w, h), interpolation=cv2.INTER_CUBIC)

    # load all of the sub images
    average_colors_for_images = []
    sub_images = []
    sub_image_list = os.listdir(args.sub_images_dir)
    for sub_image_filename in sub_image_list:
        sub_image_path = args.sub_images_dir + '/' + sub_image_filename
        sub_image = cv2.imread(sub_image_path)
        sub_image = cv2.resize(sub_image, (sub_size, sub_size), interpolation=cv2.INTER_CUBIC)
        sub_image_avg_by_color = list(np.average(np.average(sub_image, axis=0), axis=0))
        average_colors_for_images.append(sub_image_avg_by_color)
        sub_images.append(sub_image)

    # load all of the sub image color averages into the nearest neighbors structured space
    KNN_space = NearestNeighbors(n_neighbors=num_nearest_neighbors, algorithm='ball_tree').fit(average_colors_for_images)  # chosen over kd_tree based on performance tests

    # now flatten the (resized) base image so we can submit all of the points and get their nearest neighbors
    base_image = np.reshape(base_image, [-1, 3])  # [h * w, 3]
    _, nn_indices = KNN_space.kneighbors(base_image)  # first return value is nn_distances, which would be unused

    # if we are allowing for a random choice from nearest neighbors, we make those choices now.
    # this allows for more dynamic images rather than large swathes of same sub-images in a similarly colored area.
    randomly_selected_indices = np.random.randint(0, num_nearest_neighbors, size=[nn_indices.shape[0], 1])
    chosen_nn_indices = np.take_along_axis(nn_indices, randomly_selected_indices, axis=-1)

    # now we reshape the results to be of the original image shape
    chosen_nn_indices = np.reshape(chosen_nn_indices, [h, w])

    # allocate space for the output image and iteratively copy the views of each corresponding sub image to each pixel
    # todo: is there a more efficient way to do this?
    output_image = np.zeros(shape=[h * sub_size, w * sub_size, 3], dtype=np.float32)
    for r in range(h):
        for c in range(w):
            output_image[r*sub_size:(r+1)*sub_size, c*sub_size:(c+1)*sub_size, :] = sub_images[chosen_nn_indices[r,c]]

    # shove output_image back into uint8 space
    output_image=np.round(np.clip(output_image, 0, 255)).astype(np.uint8)
    cv2.imwrite('output.png', output_image)