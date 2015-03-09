packages=( 
    python-matplotlib,
    python-numpy 
)

for package in "${packages[@]}"
do
	sudo apt-get install -y $package
done

cur_dir=$( basename "$1" )
if [ cur_dir == scripts]; then
    cd ..
fi

python setup.py install --user
