# blunt-facts

## Gen strain info

`python genstraininfo -s 'laughing buddha'`

## Gen strain NFT

```
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --upgrade Pillow
python laughingbuddha

PYTHONPATH=./ python genbluntfactsnft
```


# Next steps

- Manually upload image to s3
- Create cloud function gen_blunt_facts_nft
  - accept imgUrl param (point to s3 image)
  - accept strain name
  - output generated NFT
- Use web3 to list item on holaplex / metaplex