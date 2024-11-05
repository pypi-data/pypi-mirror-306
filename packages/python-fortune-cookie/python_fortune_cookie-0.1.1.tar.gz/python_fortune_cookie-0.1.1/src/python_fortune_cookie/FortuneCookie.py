import random

def quoteGetter(fortuneAmount):
    """Retrieves random good or bad fortunes based on user input and prints them.
   
    Args:
        fortuneAmount(int): number of fortunes
    
    Returns: list of randomly generated fortunes based on user input.
    """
    #maybe edit to pass file to lists o we don't open/clsoe on each
    fortunes = 0
    list = []
    while fortunes < fortuneAmount:
        print("What kind of fortune do you want? ")
        fortuneType = input("Type G for Good, Type B for Bad: ") 
        fortunes+=1
        if fortuneType == "g" or fortuneType == "G":
            lines = open("GoodFortune.txt").read().splitlines()
            choice = random.choice(lines)
            list.append(choice)
            print(choice + "\n")

        elif fortuneType == "b" or fortuneType == "B":
            lines = open("BadFortune.txt").read().splitlines()
            choice = random.choice(lines)
            list.append(choice)
            print(choice + "\n")
        
        else : 
            print("Please pick a valid option (G or B) \n")
            fortunes-=1
    return list

def customFortuneCookie(userQuote) :
    """Prints image of fortune cookie with quote.

    Args:
        userQuote(String): custom user quote

    Returns: True if image is printed
    """
    fortune_cookie_image = f"""                                                                                                    
                                                                                                        
                                                                                                        
                                                                                 
                                .@@*#@+%#...........                                                 
                            ..@*+=========####*++@@@..                                                
                            .@@==--===+==--===#=======+++.                                              
                        .@+==------==*@=---=@#===----==+@.                                            
                        .@===-:::::--==+%%=---==+==------==+@.                           =@@-=#@        
                    @-==--::---:-===+#*=---=====---:---==++.              .:@=@%=...........%.       
                    +@===---------=====@*=-----==----::--====%....... @@:.=++:................@.       
                    @===---------======*@*=----------:::@--====@@%#=%.........................:@        
                .@===--------==@=====@%@=---------::::---====@%@..........................:+=*        
                =#===-------=========+#*@=-------:::::---=====+*+...>{userQuote}....#.        
                :@==--------==========%%@=----------::----====+@#=...........................=@.        
                @==-------====*======@%@==--------:::----=====+@#...........................-*-.        
                @==-------==+%#===-==+##@=-------::::---======+*%=..........==###%@%##-..==#@@@..        
                @==-------==+#*#=====#@@@=@-----:::::---==-====@@@..........==@@@*=*@@=...........        
                @==-----====+#+=====#@@=*=----::-::---======++@#+%@%@+........                            
                %+==----===#+#=====##@..%=------::----======+=@%..                                         
                #+=========#@*==+@@@....=----:::::---=======+@@...                                         
                .@*++========%+++@%......@=--::::::-@====@=++@@..                                            
                %+++######+++@@...     .+=--::::--=======+%@@...                                            
                @+#@@##++@@.           .@-::----======+++-#@..                                              
                .*+#@#@   ..           @=#@--=======@+#=@+%...                                              
                                    @=@=======+++@@@#@:.                                                 
                                    @+===+%=+++#%@@+@..                                                  
                                    ++=====##@#@#@@@..                                                   
                                    .#+++##@@%%@@@....                                                   
                                    .##%@@@@@@#@...                                                      
                                    .:+@*@@@+@.                                                          
                                    .. %@@@...                                                           
                                                                                                        
                                                                                                        
                                                                                                        
                                                                                                        """
    #credit to https://www.asciiart.eu/image-to-ascii for conversion of a regular image of a fortune cookie to ASCII image
    print(fortune_cookie_image)
    return True

def fortuneCookie():
    """Prints image of fortune cookie without quote.

    Returns: True if image is printed
    """
    fortune_cookie_image = f"""                                                                                                    
                                                                                                        
                                                                                                        
                                                                                 
                                .@@*#@+%#...........                                                 
                            ..@*+=========####*++@@@..                                                
                            .@@==--===+==--===#=======+++.                                              
                        .@+==------==*@=---=@#===----==+@.                                            
                        .@===-:::::--==+%%=---==+==------==+@.                           =@@-=#@        
                    @-==--::---:-===+#*=---=====---:---==++.              .:@=@%=...........%.       
                    +@===---------=====@*=-----==----::--====%....... @@:.=++:................@.       
                    @===---------======*@*=----------:::@--====@@%#=%.........................:@        
                .@===--------==@=====@%@=---------::::---====@%@..........................:+=*        
                =#===-------=========+#*@=-------:::::---=====+*+............................#.        
                :@==--------==========%%@=----------::----====+@#=...........................=@.        
                @==-------====*======@%@==--------:::----=====+@#...........................-*-.        
                @==-------==+%#===-==+##@=-------::::---======+*%=..........==###%@%##-..==#@@@..        
                @==-------==+#*#=====#@@@=@-----:::::---==-====@@@..........==@@@*=*@@=...........        
                @==-----====+#+=====#@@=*=----::-::---======++@#+%@%@+........                            
                %+==----===#+#=====##@..%=------::----======+=@%..                                         
                #+=========#@*==+@@@....=----:::::---=======+@@...                                         
                .@*++========%+++@%......@=--::::::-@====@=++@@..                                            
                %+++######+++@@...     .+=--::::--=======+%@@...                                            
                @+#@@##++@@.           .@-::----======+++-#@..                                              
                .*+#@#@   ..           @=#@--=======@+#=@+%...                                              
                                    @=@=======+++@@@#@:.                                                 
                                    @+===+%=+++#%@@+@..                                                  
                                    ++=====##@#@#@@@..                                                   
                                    .#+++##@@%%@@@....                                                   
                                    .##%@@@@@@#@...                                                      
                                    .:+@*@@@+@.                                                          
                                    .. %@@@...                                                           
                                                                                                        
                                                                                                        
                                                                                                        
                                                                                                        """
    #credit to https://www.asciiart.eu/image-to-ascii for conversion of a regular image of a fortune cookie to ASCII image
    print(fortune_cookie_image)
    return True

def randomFortuneCookie(fortuneAmount) :
    """Prints a number of randomly generated fortune cookies.

    Args:
        fortuneAmount(int): the amount of fortunes 

    Returns: True if method if successful, False otherwise
    """

    if fortuneAmount > 5:
        print("fortune amount exceeds 5")
        return False

    good = open("GoodFortune.txt").read().splitlines()
    bad = open("BadFortune.txt").read().splitlines()

    for i in range(fortuneAmount):

        choices = good + bad

        random_choice = random.choice(choices)

        customFortuneCookie(random_choice)
    return True

def addQuote(userQuote, quoteType): 
    """Adds a custom user quote to the file.

    Args:
        userQuote(String): custom user quote
        quoteType(String): good or bad quote (everything but g/G is considered bad)

    Returns: True if method is successful
    """
    fortuneType = quoteType

    if fortuneType == "g" or fortuneType == "G":
        f = open("GoodFortune.txt", "a")
        f.write(userQuote + "\n")
        f.close()
    else:
        f = open("BadFortune.txt", "a")
        f.write(userQuote + "\n")
        f.close()
    return True

def cookieScript(fortuneCustom):
    """A simulated process of getting fortunes. Param is c to create your own fortune cookie or r for random.

    Args:
        fortuneCustom(String): the type of fortune generation process the user wants

    Returns: True if method is successful
    """

    print("Welcome to Scooby's Fortunes!")

    if fortuneCustom == "c":
        userQuote = input("Enter your custom fortune: ")
        customFortuneCookie(userQuote)
        #might be too similar to other fortune cookie functions could change to have params be c or p and then do either customCookie or the code below for purchase

    else:
        fortuneAmount = int(input("You can have up to 10 so how many fortune cookies do you want: "))

        while fortuneAmount < 0 or fortuneAmount > 10:
            print("Inavlid Fortune amount, try again.")
            fortuneAmount = int(input("You can have up to 10 so how many fortune cookies do you want: "))

        else:
            if fortuneAmount == 0:
                print("Sad to see you go.")
            else:
                if fortuneAmount < 6:
                    fortuneRandom = input("Would you like to pick the type of random fortune, yes or no: ")
                    if fortuneRandom == "no":
                        randomFortuneCookie(fortuneAmount)
                    elif fortuneRandom == "yes":
                        #credit to https://www.houstonpress.com/restaurants/fortune-cookie-sayings-youd-never-want-to-get-6412278 for bad fortunes
                        #credit to https://www.quora.com/If-you-were-a-fortune-cookie-writer-what-funny-and-unexpected-fortunes-would-you-include for bad fortunes
                        quoteGetter(fortuneAmount)
                        fortuneCookie()
                        
                else: 
                    quoteGetter(fortuneAmount)
                    fortuneCookie()

    print("Goodbye!")

    return True

