# Setting Up the Environment

This app uses `.env` files to store secrets. Both the backend as well as the frontend use this.

## Backend

Copy the `.env.example` to `.env` and fill in the required variables

> [!NOTE]
>
> 1.  `DATABASE_URL`: Put your username and password in the database connection strings.
> 1.  `SSO_CLIENT_ID` and `SSO_CLIENT_SECRET`: You will have to go to `https://gymkhana.iitb.ac.in/profiles`, create an app and get the CLIENT_ID and CLIENT_SECRET from there.
> 1.  `SSO_AUTHORIZATION_HEADER_B64`: You will have to base64 encode the string of the format `CLIENT_ID:CLIENT_SECRET` using any cmd line tool such as `base64` or any other online tool.

## Frontend

Copy the `.env.example` to `.env.local` and fill in the required variables

> [!NOTE]
>
> 1.  `NEXT_PUBLIC_SSO_URL`: You will have to fill in the client ID you acquired for the backend in this url (replace `<client-id>` with the client ID you acquired)
