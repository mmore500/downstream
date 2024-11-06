#include "downstream/dstream/steady_algo/_steady_assign_storage_site.hpp"
#include "downstream/dstream/steady_algo/_steady_has_ingest_capacity.hpp"
#include <iostream>
#include <cstdint>
#include <optional>
#include <signal.h>

int main() {
    signal(SIGPIPE, SIG_IGN);

    std::ios_base::sync_with_stdio(false);
    int64_t T, S;

    while (std::cin >> S >> T) {

        if (steady_has_ingest_capacity(S, T)) {
            auto result = downstream::dstream::steady_algo::steady_assign_storage_site(S, T);
            if (result) {
                std::cout << *result << '\n';
            } else {
                std::cout << "None\n";
            }
            // std::cout.flush();
        } else {
            std::cout << "\n";
        }
    }

    return 0;
}