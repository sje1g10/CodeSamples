# process_results.sh
#  Make plots and put into beamer animation

python plot.py
echo
echo 'Compiling pdf animation...'
cd results/
pdflatex results.tex > temp.txt
pdflatex results.tex > temp.txt
rm temp.txt
mv results.pdf ../
cd ../

echo
echo 'Done!'
echo 'See results.pdf for animated results (view in Adobe Reader).'
