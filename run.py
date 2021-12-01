import katsuserver
import os


def run():
    App = katsuserver.create_app(
                            config_name=os.getenv('FLASK_CONFIG', 'default')
                        )
    App.run(debug=True)


if __name__ == '__main__':

    run()
