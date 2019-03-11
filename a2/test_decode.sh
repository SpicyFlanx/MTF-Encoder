for file in ./tests/*.mtf; do
	python3 mtf2text.py $file
done

for file in ./tests/*.txt; do
	n=$(basename "$file")
	if cmp -s $file ./tests2/$n; then
		echo $n same
	else
		echo $n different
	fi
done 

