all:
	
	pdflatex -shell-escape rapport.tex
	pdflatex -shell-escape rapport.tex

clean:
	rm -rf *bak *~ *out *log *aux _minted-rapport *.aex
