From registry.datadrivendiscovery.org/jpl/docker_images/complete:ubuntu-artful-python36-devel
ADD . /d3m-ta2
WORKDIR /d3m-ta2
RUN pip3 install -r requirements.txt
RUN pip3 uninstall -y d3m
RUN pip3 install --process-dependency-links git+https://gitlab.com/datadrivendiscovery/d3m.git@devel
