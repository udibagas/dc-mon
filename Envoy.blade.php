@servers(['dc' => ['dc@10.45.5.120', 'dc@10.45.5.121', 'dc@10.45.5.122']])

@task('deploy', ['on' => 'dc', 'parallel' => true])
    cd dc-mon
    git pull
    php artisan migrate
@endtask
