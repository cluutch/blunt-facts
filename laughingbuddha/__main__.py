from blunt_facts_nft import BluntFactsNft
from strain_info import laughing_buddha_info

INPUT_IMG_FILEPATH = "laughingbuddha/02_cropped.png"
OUTPUT_IMG_FILEPATH = "laughingbuddha/laughing-buddha-blunt-facts-03.png"


def main():


    print("Creating Laughing Buddha NFT")
    laughing_buddha_nft = BluntFactsNft(laughing_buddha_info,
                                        INPUT_IMG_FILEPATH,
                                        OUTPUT_IMG_FILEPATH)
    laughing_buddha_nft.gen_img()


if __name__ == '__main__':
    main()
