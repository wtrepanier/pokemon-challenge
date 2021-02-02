from push_api.crawling import get_pokemons
from push_api.push_to_coveo import push_pokemons


def main():
    push_pokemons(get_pokemons())


if __name__ == "__main__":
    main()
