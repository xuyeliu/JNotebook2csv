import os
import nbformat
import csv
import pandas
import argparse
import sys
def getFiles(dir, suffix): # 查找根目录，文件后缀 
    res = []
    for root, directory, files in os.walk(dir):  # =>当前根,根下目录,目录下的文件
        for filename in files:
            name, suf = os.path.splitext(filename) # =>文件名,文件后缀
            if suf == suffix:
                res.append(os.path.join(root, filename)) # =>吧一串字符串组合成路径
    return res


def exportNotebook(notebook, filename):
    rows = []
    for index, cell in enumerate(notebook.cells):
        code = cell['source']
        ctype = cell['cell_type']
        row = [index, code, ctype, '', '']
        rows.append(row)
    
    fields = ['ID', 'Source', 'Type', 'Category', 'Stage']
    
    # writing to csv file  
    with open(filename, 'w') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
        
        # writing the fields  
        csvwriter.writerow(fields)  
        
        # writing the data rows  
        csvwriter.writerows(rows)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--infile', dest='infile', type=str, default=None)
    parser.add_argument('--indir', dest='indir', type=str, default=None)
    parser.add_argument('--outdir', dest='outdir', type=str, default=None)
    parser.add_argument('--outfile', dest='outfile', type=str, default=None)
    args = parser.parse_args()
    infile = args.infile
    indir = args.indir
    outdir = args.outdir
    outfile = args.outfile

    if indir and outdir and not infile and not infile:
        file_list = getFiles(indir, '.ipynb')
        for file in getFiles(indir, '.ipynb'):  # =>查找以.py结尾的文件
            print(file)

        for n_index, notebook in enumerate(file_list):
            namelist = notebook.split('/')
            name = namelist[-1].split('.')[0]
            jake_notebook = nbformat.read(notebook , as_version=4)
            file_name = outdir + name + '.csv'
            exportNotebook(jake_notebook, file_name)
            print(file_name)
    
    elif outfile or outdir and infile:
        if outfile and outdir:
            print("input type incorrect!")
            sys.exit()
        elif outfile:
            jake_notebook = nbformat.read(infile , as_version=4)
            exportNotebook(jake_notebook, outfile)
        elif outdir:
            namelist = infile.split('/')
            name = namelist[-1].split('.')[0]
            jake_notebook = nbformat.read(infile , as_version=4)
            exportNotebook(jake_notebook, outdir+name+".csv")
    
    else:
        print("input type incorrect!")
        sys.exit()
