<template>
    <div class="container">
        <div class="row">
            <div class="col-md-8 col-md-offset-2">
                <div class="panel panel-default">
                    <div class="panel-heading">Example Component</div>

                    <div class="panel-body">
                        <h1>{{ name }}</h1>
                        <h1>{{ email }}</h1>
                        <a @click="aaa()">klik me</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        mounted() {
            console.log('Component mounted.')
        },
        data: function() {
            return {
                name: "udibagas",
                email: "udibagas@gmail.com"
            }
        },
        methods: {
            aaa: function() {
                alert('aaaa')
            }
        }
    }
</script>
