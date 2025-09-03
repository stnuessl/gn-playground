#include <gtest/gtest.h>

extern "C" void io(void);

TEST(init, case01)
{
    io();
}

int main(int argc, char *argv[])
{
    ::testing::InitGoogleTest(&argc, argv);

    return RUN_ALL_TESTS();
}
