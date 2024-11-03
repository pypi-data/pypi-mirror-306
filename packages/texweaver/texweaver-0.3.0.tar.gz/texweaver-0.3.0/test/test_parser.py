from texweaver import TexParser
def test_parser():
    with open('test/test.md', 'r') as f:
        src = f.read()
    parser = TexParser()
    parser.parse(src)
    print(parser.doc.to_json())
    
if __name__ == '__main__':
    test_parser()