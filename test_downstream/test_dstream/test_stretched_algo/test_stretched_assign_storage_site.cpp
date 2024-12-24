#include <iostream>
#include <csignal>
#include "downstream/dstream/stretched_algo/_stretched_assign_storage_site.hpp"
#include "downstream/dstream/stretched_algo/_stretched_has_ingest_capacity.hpp"

using namespace downstream::dstream::stretched_algo;

int main() {
    signal(SIGPIPE, SIG_IGN);
    std::ios_base::sync_with_stdio(false);
    uint64_t T, S;

    while (std::cin >> S >> T) {
        if (stretched_has_ingest_capacity(S, T)) {
            auto result = stretched_assign_storage_site(S, T);
            if (result) {
                std::cout << *result << '\n';
            } else {
                std::cout << "None\n";
            }
        } else {
            std::cout << "\n";
        }
    }
    return 0;
}