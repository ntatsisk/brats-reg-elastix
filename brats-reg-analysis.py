import itk
from fileconfig import DATAPATH, OUTPUTPATH
import time
import shutil

# Setup the registration
parameter_object = itk.ParameterObject.New()
parameter_map_rigid = parameter_object.GetDefaultParameterMap('rigid')
parameter_map_bspline = parameter_object.GetDefaultParameterMap('bspline')
parameter_object.AddParameterMap(parameter_map_rigid)
parameter_object.AddParameterMap(parameter_map_bspline)
# parameter_object.SetParameter(0, "WriteResultImage", "false")

for subject in list(DATAPATH.iterdir()): #[:10]:
    if subject.is_dir():
        start_time = time.time()
        output_subject_path = OUTPUTPATH / subject.stem
        output_subject_path.mkdir(exist_ok=True)
        
        image_files = [item for item in subject.iterdir() if item.is_file() and 't1ce' in item.name]
        landmark_files = [item for item in subject.iterdir() if item.is_file() and 'landmarks' in item.name]

        # Copy flair images and landmarks directly to result folders
        for f in image_files + landmark_files:
            shutil.copy(str(f), str(output_subject_path / f.name))

        fixed_image = itk.imread(str(image_files[0]), itk.F)
        moving_image = itk.imread(str(image_files[1]), itk.F)

        # Register and write results
        result_image, result_transform_parameters = itk.elastix_registration_method(fixed_image, moving_image,
                                                                                    parameter_object=parameter_object,
                                                                                    log_to_console=False,
                                                                                    log_to_file=True,
                                                                                    log_file_name="log.txt",
                                                                                    output_directory=str(output_subject_path))

        end_time = time.time()
        print(f"Subject {subject.stem}: {end_time - start_time} sec")