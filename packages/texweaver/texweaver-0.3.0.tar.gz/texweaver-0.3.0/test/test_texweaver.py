from texweaver import TexParser
from texweaver import DefaultConfig
def test_parser():
    with open('test/test.md', 'r') as f:
        src = f.read()
    
    parser = TexParser()
    parser.parse(src)
    mdoc = parser.doc
    latex = mdoc.to_latex(DefaultConfig)
    print(latex)
    
if __name__ == '__main__':
    test_parser()