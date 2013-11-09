hyves-username-grab
===================

http://archiveteam.org/index.php?title=Hyves

Running without a warrior
-------------------------

To run this outside the warrior:

(Ubuntu / Debian 7)

    sudo apt-get update
    sudo apt-get install -y python python-setuptools python-dev git-core python-pip rsync git screen
    pip install --user seesaw
    git clone https://github.com/ArchiveTeam/hyves-username-grab
    cd hyves-username-grab
    
    # Start downloading with:
    screen ~/.local/bin/run-pipeline --disable-web-server pipeline.py YOURNICKNAME

(Debian 6)

    sudo apt-get update
    sudo apt-get install -y python python-setuptools python-dev git-core python-pip rsync git screen
    wget --no-check-certificate https://pypi.python.org/packages/source/p/pip/pip-1.3.1.tar.gz
    tar -xzvf pip-1.3.1.tar.gz
    cd pip-1.3.1
    python setup.py install --user
    cd ..
    ~/.local/bin/pip install --user seesaw
    git clone https://github.com/ArchiveTeam/hyves-username-grab
    cd hyves-username-grab

    # Start downloading with:
    screen ~/.local/bin/run-pipeline --disable-web-server pipeline.py YOURNICKNAME

(CentOS / RHEL / Amazon Linux)

    sudo yum install python-devel python-distribute git rsync screen
    wget --no-check-certificate https://pypi.python.org/packages/source/p/pip/pip-1.3.1.tar.gz
    tar -xzvf pip-1.3.1.tar.gz
    cd pip-1.3.1
    python setup.py install --user
    cd ..
    ~/.local/bin/pip install --user seesaw
    git clone https://github.com/ArchiveTeam/hyves-username-grab
    cd hyves-username-grab

    # Start downloading with:
    screen ~/.local/bin/run-pipeline --disable-web-server pipeline.py YOURNICKNAME

For more options, run:

    ~/.local/bin/run-pipeline --help

If the wget script complains about GNUTLS, please install `libgnutls-dev` as well (`gnutls-devel` on Fedora).

