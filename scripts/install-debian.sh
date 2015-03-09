packages=( 
    python-matplotlib,
    python-numpy 
    ipython-notebook
)

for package in "${packages[@]}"
do
	sudo apt-get install -y $package
done

inst () {
    cd .. &&  python setup.py install --user
}

cur_dir=$( basename "$1" )
if [ cur_dir == "scripts" ]; then
    inst
fi
