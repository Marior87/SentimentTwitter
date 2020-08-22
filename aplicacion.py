import analisis

from argparse import ArgumentParser


def build_argparser():
    """
    Parse command line arguments.
    :return: command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument("-q", "--query", required=True, type=str,
                        help="Query de búsqueda en Twitter")

    return parser


def main():
    """
    Load the network and parse the output.
    :return: None
    """
    # Obtenemos argumentos de la línea de comandos:
    args = build_argparser().parse_args()

    # Realizamos el análisis:
    final_score, lista_tweets = analisis.analyze_tweets(
        args.query, total_tweets=10)

    for tweet in lista_tweets:
        print(tweet)

    print("Puntaje Final: ", final_score)


if __name__ == '__main__':
    main()
