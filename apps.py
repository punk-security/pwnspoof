from models import App
import activity_patterns as ap

banking = App("bankofpunk.local")

banking.set_dynamic_activity_pattern(ap.Banking.dynamic_routine_use)
banking.noise_interactions += list(ap.Misc.noise)
banking.attacks["bruteforce"] = ap.Banking.dynamic_brute_force
banking.attacks["command_injection"] = ap.Misc.dynamic_cmd_injectiom

wordpress = App("apunksblog.local")
wordpress.set_dynamic_activity_pattern(ap.Wordpress.dynamic_browse_or_admin)
wordpress.noise_interactions += ap.Wordpress.noise
wordpress.attacks["bruteforce"] = ap.Wordpress.dynamic_brute_force
wordpress.attacks["command_injection"] = ap.Wordpress.dynamic_malicious_plugin

apps = {"banking": banking, "wordpress": wordpress}
