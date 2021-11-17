export default function ({ app, redirect }) {
    if(!app.$cookies.get("session"))
        return redirect("/");
}