from models import App
import activity_patterns as ap

banking = App("bankofpunk.local")

banking.set_dynamic_activity_pattern(ap.Banking.dynamic_routine_use)
banking.noise_interactions += list(ap.Misc.noise)
banking.attacks["bruteforce"] = ap.Banking.dynamic_brute_force
banking.attacks["command_injection"] = ap.Misc.dynamic_cmd_injectiom

apps = {
    "banking": banking,
}
