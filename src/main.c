/*
 * How many programmers does it take to change a light bulb?
 * None. That’s a hardware problem.
 */

#include "core/core.h"
#include "drivers/drivers.h"
#include "init/init.h"
#include "io/io.h"
#include "utils/utils.h"

#ifdef GN_UNITTEST
#define main ut_main
#endif

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;

    init();
    core();
    drivers();
    utils();
    io();

    return 0;
}
