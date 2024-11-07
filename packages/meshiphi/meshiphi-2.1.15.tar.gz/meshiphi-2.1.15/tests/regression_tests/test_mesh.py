"""
    Regression testing package to ensure consistent functionality in development
    of the PolarRoute python package.
"""

import json
import pytest
import time
import os

import meshiphi

# Import tests, which are automatically run

from .mesh_test_functions import test_mesh_cellbox_attributes
from .mesh_test_functions import test_mesh_cellbox_count
from .mesh_test_functions import test_mesh_cellbox_ids
from .mesh_test_functions import test_mesh_cellbox_values
from .mesh_test_functions import test_mesh_neighbour_graph_count
from .mesh_test_functions import test_mesh_neighbour_graph_ids
from .mesh_test_functions import test_mesh_neighbour_graph_values


import logging
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


#File locations of all environmental meshes to be recalculated for regression testing.
TEST_ENV_MESHES = [
    './example_meshes/env_meshes/grf_normal.json',
    './example_meshes/env_meshes/grf_downsample.json',
    './example_meshes/env_meshes/grf_reprojection.json',
    './example_meshes/env_meshes/grf_sparse.json'
]

TEST_ABSTRACT_MESHES = [
    './example_meshes/abstract_env_meshes/vgrad.json',
    './example_meshes/abstract_env_meshes/hgrad.json',
    './example_meshes/abstract_env_meshes/checkerboard_1.json',
    './example_meshes/abstract_env_meshes/checkerboard_2.json',
    './example_meshes/abstract_env_meshes/checkerboard_3.json',
    './example_meshes/abstract_env_meshes/circle.json',
    './example_meshes/abstract_env_meshes/circle_quadrant_split.json',
    './example_meshes/abstract_env_meshes/circle_quadrant_nosplit.json'
]

def setup_module():
    LOGGER.info(f'MeshiPhi version: {meshiphi.__version__}')

@pytest.fixture(scope='session', autouse=False, params=TEST_ENV_MESHES + TEST_ABSTRACT_MESHES)
def mesh_pair(request):
    """
    Creates a pair of JSON objects, one newly generated, one as old reference
    Args:
        request (fixture):
            fixture object including list of meshes to regenerate

    Returns:
        list: old and new mesh jsons for comparison
    """

    
    LOGGER.info(f'Test File: {request.param}')
   

    with open(request.param, 'r') as fp:
        old_mesh = json.load(fp)
    
    mesh_config = old_mesh['config']['mesh_info']
    new_mesh = calculate_env_mesh(mesh_config)
    
    test_name = os.path.basename(request.param)

    return {"test": test_name,
            "old_mesh": old_mesh,
            "new_mesh": new_mesh}

def calculate_env_mesh(mesh_config):
    """
    Creates a new environmental mesh from the old mesh's config

    Args:
        mesh_config (json): Config to generate new mesh from

    Returns:
        json: Newly regenerated mesh
    """
    start = time.perf_counter()

    mesh_builder = meshiphi.MeshBuilder(mesh_config)
    new_mesh = mesh_builder.build_environmental_mesh()

    end = time.perf_counter()
    
    cellbox_count = len(new_mesh.agg_cellboxes)
    LOGGER.info(f'Mesh containing {cellbox_count} cellboxes built in {end - start} seconds')


    return new_mesh.to_json()


def test_record_output(mesh_pair, tmp_path):
    """
    Store fixtures after they're generated to avoid having to recompute
    meshes for diagnosis upon failure

    Args:
        mesh_pair (dict): 
            Fixture holding generated meshes
        tmp_path (fixture): 
            Pytest built-in fixture that creates a unique temporary directory
            for this test's run
    """

    test_name = mesh_pair['test']
    test_basename = test_name.split('.')[0]
    # Save files to folder above where pytest would normally save, since tmp_path is the directory
    # we want to scrape later. Otherwise, pytest will add subdirectories which overwrite eachother
    # after 3 tests, and it's possible for more than 3 tests to be run in one pytest call
    # Ref: https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html#the-default-base-temporary-directory
    save_filename = os.path.join(tmp_path, '..', f'{test_basename}.comparison.json')

    # Only care about the meshes used as a fixture
    meshes = {key: val for key, val in mesh_pair.items() if key != 'test'}

    # Output as a json
    with open(save_filename,'w') as fp:
        json.dump(meshes, fp, indent=4)
