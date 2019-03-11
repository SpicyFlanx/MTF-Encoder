for file in ./tests/*.txt; do
	python3 text2mtf.py $file
done

for file in ./tests/*.mtf; do
	n=$(basename "$file")
	if diff -s $file ./tests2/$n; then
		:
	else
		echo $n different
	fi
done 

