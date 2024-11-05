import python_fortune_cookie.FortuneCookie as FortuneCookie

def main():
    option = input("Do you want to generate random fortunes or create your own? (r for random, c for create): ")

    if option != "c" and option != "r":
        print("Invalid options")
    else: 
        FortuneCookie.cookieScript(option)


if __name__ == "__main__":
    main()