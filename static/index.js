window.app = new Vue({
    el: '#app',
    data: {
        token: null,
        response: null
    },
    delimiters: ['[[',']]'],
    methods: {
        logout: function(event){
            axios
                .post('/api/logout')
            this.token = null
            localStorage.setItem('TOKEN',null)
        },
        showlogin: function(event){
            console.log("Implement me")
        },
        login: function(event){
            var email = document.getElementById('input_email_login').value
            var password = document.getElementById('input_password_login').value
            var pack = {
                'email': email,
                'password': password
            }
            axios
                .post('/api/login',pack)
                .then(
                    resp=>{
                        if(resp.data['code'] == 200){
                            self.token = "s"
                            localStorage.setItem('TOKEN',resp.data['sessionID'])
                            this.token = localStorage.getItem('TOKEN')
                            this.response = null
                        }else{
                            this.response = resp.data['message']
                            this.token = null
                        }
                    }
                )
        },
        dotfiles: function(event){
            console.log("implement me")
        }
    },
    created(){
        if(localStorage.getItem('TOKEN') == 'null'){
            this.token = null
        }else{
            this.token = localStorage.getItem('TOKEN')
        }
    }
})