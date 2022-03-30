from Generator import Generator
import sys
import secrets

def main(seed):
    generator = Generator(seed)
    generator.run()


if __name__ == '__main__':
    if (len(sys.argv[1:]) < 1):
        seed = secrets.token_urlsafe(8)
    else:
        seed = sys.argv[1]
    main(seed)