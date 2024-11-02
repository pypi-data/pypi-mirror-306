from initialize import  initialize
from data import get_historical_yield_data


if __name__ == "__main__":

    print("----")

    initialize("6X9oFeB88pTLdeTcg997uCodlNFP9l1D")

    data = get_historical_yield_data(
        crop="soybeans",
        year=2010,
        country='US',
        spatial_resolution='state'
    )
    print(data)

    print("----")

