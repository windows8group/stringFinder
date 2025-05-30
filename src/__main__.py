from . import main
import faulthandler

if __name__ == "__main__":
    faulthandler.enable()
    main.main()