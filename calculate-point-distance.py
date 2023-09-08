import pandas as pd
from sklearn.metrics import median_absolute_error as MAE
import numpy as np
import itk
from fileconfig import OUTPUTPATH
import time
import pandas as pd
import matplotlib.pyplot as plt

subjects = []
initial_distances = []
result_distances = []

for subject in list(OUTPUTPATH.iterdir()):
    if subject.is_dir():
        start_time = time.time()        
        image_files = [item for item in subject.iterdir() if item.is_file() and 't1ce' in item.name]
        landmark_files = [item for item in subject.iterdir() if item.is_file() and 'landmarks' in item.name]

        # Load the moving image for the reference frame
        moving_image = itk.imread(str(image_files[1]), itk.F)

        # Load the landmarks
        fixed_landmarks = pd.read_csv(str(landmark_files[0]), header=0, index_col=0).to_numpy().astype(np.float64)
        moving_landmarks = pd.read_csv(str(landmark_files[1]), header=0, index_col=0).to_numpy().astype(np.float64)

        # Convert to list of lists
        fixed_landmarks_list = [list(point) for point in fixed_landmarks]
        moving_landmarks_list = [list(point) for point in moving_landmarks]

        # Compute distance (both sets are defined in the same coordinate space)
        dist = MAE(fixed_landmarks_list, moving_landmarks_list)
        
        # Create mesh to store the landmarks
        fixed_landmarks_mesh = itk.Mesh[itk.F, 3].New()
        for i, landmark in enumerate(fixed_landmarks):
            fixed_landmarks_mesh.SetPoint(i, landmark)

        # Load transform parameters from file
        result_transform_parameters = itk.ParameterObject.New()
        # result_transform_parameters.ReadParameterFile(str(subject / "TransformParameters.0.txt"))
        result_transform_parameters.ReadParameterFile(str(subject / "TransformParameters.1.txt"))

        # Transform the landmarks based on the previous registration result
        transformix_filter = itk.TransformixFilter.New(moving_image)
        transformix_filter.SetTransformParameterObject(result_transform_parameters)
        transformix_filter.SetInputMesh(fixed_landmarks_mesh)
        transformix_filter.Update()
        result_landmarks_mesh = transformix_filter.GetOutputMesh()

        # Compute distance of transformed points
        result_landmarks_list = [list(result_landmarks_mesh.GetPoint(i)) 
                                 for i in range(result_landmarks_mesh.GetNumberOfPoints())]
        result_dist = MAE(result_landmarks_list, moving_landmarks_list)
        print(f"Subject {subject.stem} | Initial: {dist} - Final: {result_dist}")

        # Store results
        subjects.append(subject.stem)
        initial_distances.append(dist)
        result_distances.append(result_dist)

        end_time = time.time()
        # print(f"Subject {subject.stem}: {end_time - start_time} sec")

# Store results as .csv
df_results = pd.DataFrame({'subject': subjects, 
                           'initial_distance': initial_distances, 
                           'result_distance': result_distances})
df_results.to_csv(str(OUTPUTPATH / "result_distances.csv"))

# Show reults
df_results.set_index('subject', inplace=True)
df_results.boxplot()
plt.savefig(str(OUTPUTPATH / "results_boxplot.png"))
plt.show()