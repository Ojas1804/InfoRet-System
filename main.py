from Query import Query
from SoundexIndex import SoundexIndex

def main():
    print("========PLEASE READ THE README FILE BEFORE RUNNING THE PROGRAM========")
    # test biword index and normal index
    print("The given example tests biword index and normal index")
    query = Query("(world war and war) or (bosnian and not war) or (colonial and empires)")
    # query = Query("indian national congress or german invade")
    print("QUERY  =  ", query.query)
    print(query.process_query())

    # test soundex index
    soundex_index = SoundexIndex()
    print()
    print("The given example tests soundex index")
    query = "wurlt and wer"
    print("QUERY  =  ", query)
    print(soundex_index.test_query(query))

if __name__ == "__main__":
    main()