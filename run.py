import katsuserver
import os


if __name__ == '__main__':
    App = katsuserver.create_app(
                            config_name=os.getenv('FLASK_CONFIG', 'default')
                        )
    App.run(debug=False)
