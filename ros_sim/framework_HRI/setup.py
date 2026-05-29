from setuptools import find_packages, setup
from glob import glob


package_name = 'framework_HRI'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
         ('share/framework_HRI/launch', glob('launch/*.py')),
         ('share/' + package_name + '/meshes',
    glob('meshes/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fatemeh',
    maintainer_email='fatemeh.rastgar2@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        "bernstein_coeff_order10_arbitinterval = framework_HRI.bernstein_coeff_order10_arbitinterval:main",
        "expert_interrupt = framework_HRI.expert_interrupt:main",
        "run_continuous = framework_HRI.run_continuous:main",
        "ContinuousExecutor = framework_HRI.ContinuousExecutor:main",
        "world_con = framework_HRI.world_con:main",
        "world_state_builder_continuous = framework_HRI.world_state_builder_continuous:main",
        "local_planner_priest_interrupt = framework_HRI.local_planner_priest_interrupt:main",
        "task_planner_interrupt = framework_HRI.task_planner_interrupt:main",
        "planner_2 = framework_HRI.planner_2:main",
        "planner_3 = framework_HRI.planner_3:main",
        ],
    },
)
