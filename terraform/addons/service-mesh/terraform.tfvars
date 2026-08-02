subscription_id = "3a15b2d9-99f7-48fa-a6c6-9ebd7ff7a153"

applications = {

  tic-tac-toe = {

    service_port   = 80
    canary_enabled = false

    primary = {
      version = "v1"
      weight  = 100
    }

    canary = {
      version = "v2"
      weight  = 0
    }

  }

  tetris = {

    service_port   = 80
    canary_enabled = false

    primary = {
      version = "v1"
      weight  = 100
    }

    canary = {
      version = "v2"
      weight  = 0
    }

  }

}