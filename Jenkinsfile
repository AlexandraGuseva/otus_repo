pipeline {
    agent any

    parameters {
        string(name: 'SELENOID_URL', defaultValue: 'http://host.docker.internal:4444/wd/hub', description: 'Адрес Selenoid')
        string(name: 'BASE_URL', defaultValue: 'http://host.docker.internal:8080', description: 'Адрес PrestaShop')
        choice(name: 'BROWSER', choices: ['firefox', 'chrome'], description: 'Браузер')
        string(name: 'BROWSER_VERSION', defaultValue: '120.0', description: 'Версия браузера')
        string(name: 'THREADS', defaultValue: '1', description: 'Количество потоков')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'hw_docker', url: 'https://github.com/AlexandraGuseva/otus_repo.git'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'mkdir -p allure-results'

                sh """
                    docker run --rm \
                    --network selenoid \
                    -e SELENOID_URL=${params.SELENOID_URL} \
                    -v "\$(pwd)/allure-results:/app/allure-results" \
                    otus_repo-tests \
                    --browser=${params.BROWSER} \
                    --base_url=${params.BASE_URL} \
                    --alluredir=/app/allure-results
                """
            }
        }
    }

    post {
        always {
            // Генерация отчета Allure
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}