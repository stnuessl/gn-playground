#include <gtest/gtest.h>

extern "C" {

void ut_main(void);

void core(void)
{}

void drivers(void)
{}

void init(void)
{}

void io(void)
{}

void utils(void)
{}
}

TEST(main, case01)
{
    ut_main();
}

int main(int argc, char *argv[])
{
    ::testing::InitGoogleTest(&argc, argv);

    return RUN_ALL_TESTS();
}
