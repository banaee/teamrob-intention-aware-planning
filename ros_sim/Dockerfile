FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV PYTHONUNBUFFERED=1

# Basic Ubuntu tools and locale configuration
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    curl \
    ca-certificates \
    software-properties-common \
    && locale-gen en_US en_US.UTF-8 \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && add-apt-repository universe \
    && rm -rf /var/lib/apt/lists/*

# Configure the official ROS 2 apt repository
RUN ROS_APT_SOURCE_VERSION=$( \
        curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest \
        | grep -F '"tag_name"' \
        | awk -F'"' '{print $4}' \
    ) \
    && curl -L \
        -o /tmp/ros2-apt-source.deb \
        "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.jammy_all.deb" \
    && apt-get update \
    && apt-get install -y /tmp/ros2-apt-source.deb \
    && rm /tmp/ros2-apt-source.deb

# Install ROS 2 Humble and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-ros-base \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-pip \
    python3-venv \
    build-essential \
    cuda-cupti-12-4 \
    && rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH="/usr/local/cuda-12.4/extras/CUPTI/lib64:/usr/local/cuda/extras/CUPTI/lib64:${LD_LIBRARY_PATH}"

# Initialize rosdep
RUN rosdep init && rosdep update

# Create a virtual environment that can still access ROS Python packages
RUN python3 -m venv --system-site-packages /opt/venv

ENV PATH="/opt/venv/bin:${PATH}"

# Install JAX and other Python dependencies
COPY requirements.txt /tmp/requirements.txt

RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install --no-cache-dir -r /tmp/requirements.txt

# Create a ROS workspace and copy this package into it
WORKDIR /ws

COPY . /ws/src/framework_hri_package

# Install dependencies declared in package.xml
RUN apt-get update \
    && source /opt/ros/humble/setup.bash \
    && rosdep install \
        --from-paths /ws/src \
        --ignore-src \
        --rosdistro humble \
        -r -y \
    && rm -rf /var/lib/apt/lists/*

# Build the ROS package
RUN source /opt/ros/humble/setup.bash \
    && colcon build --symlink-install

COPY docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["bash"]
