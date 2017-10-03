<?php $__container->servers(['dc' => ['dc@10.45.5.120', 'dc@10.45.5.121', 'dc@10.45.5.122']]); ?>

<?php $__container->startTask('deploy', ['on' => 'dc'], 'parallel' => true); ?>
    cd dc-mon
    git pull
    php artisan migrate
<?php $__container->endTask(); ?>
