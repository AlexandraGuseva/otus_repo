pipeline {
    agent any

    parameters {
        string(name: 'SELENOID_URL', defaultValue: 'http://host.docker.internal:4444/wd/hub', description: 'Адрес Selenoid')
        string(name: 'BASE_URL', defaultValue: 'http://prestashop:80', description: 'Адрес PrestaShop')
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

        // НОВЫЙ ЭТАП: Сборка образа (чтобы не было ошибки "image not found")
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t otus_repo-tests .'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'mkdir -p allure-results'

                // Передаем аргументы так, чтобы они попали в pytest
                // --browser_version и --threads - это наши новые параметры
                // -n ${params.THREADS} - это аргумент для pytest-xdist
                sh """
                    docker run --rm \
                    --network selenoid \
                    -e SELENOID_URL=${params.SELENOID_URL} \
                    -v "\$(pwd)/allure-results:/app/allure-results" \
                    otus_repo-tests \
                    tests/ \
                    --browser=${params.BROWSER} \
                    --browser_version=${params.BROWSER_VERSION} \
                    --base_url=${params.BASE_URL.trim()} \
                    --alluredir=/app/allure-results \
                    -n ${params.THREADS} -v
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