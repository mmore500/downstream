#include <csignal>
#include <iostream>
#include <string>
#include <string_view>

#include "include/downstream/dstream/hybrid_0_steady_1_stretched_2_algo/_hybrid_assign_storage_site.hpp"
#include "include/downstream/dstream/hybrid_0_steady_1_stretched_2_algo/_hybrid_has_ingest_capacity.hpp"
#include "include/downstream/dstream/steady_algo/_steady_assign_storage_site.hpp"
#include "include/downstream/dstream/steady_algo/_steady_has_ingest_capacity.hpp"
#include "include/downstream/dstream/stretched_algo/_stretched_assign_storage_site.hpp"
#include "include/downstream/dstream/stretched_algo/_stretched_has_ingest_capacity.hpp"
#include "include/downstream/dstream/tilted_algo/_tilted_assign_storage_site.hpp"
#include "include/downstream/dstream/tilted_algo/_tilted_has_ingest_capacity.hpp"

namespace {

template<typename HasIngestFn, typename AssignStorageFn>
void process_single_input(uint64_t S, uint64_t T, HasIngestFn has_ingest, AssignStorageFn assign_storage) {
    if (has_ingest(S, T)) {
        auto result = assign_storage(S, T);
        std::cout << (result ? std::to_string(*result) : "None") << '\n';
    } else {
        std::cout << '\n';
    }
}

bool process_algorithm(const std::string_view target_function) {
    using namespace downstream::dstream;

    uint64_t T, S;
    while (std::cin >> S >> T) {
        if (target_function == "dstream.hybrid_0_steady_1_stretched_2_algo.assign_storage_site") {
            process_single_input(S, T,
                hybrid_0_steady_1_stretched_2_algo::hybrid_has_ingest_capacity,
                hybrid_0_steady_1_stretched_2_algo::hybrid_assign_storage_site);
        }
        else if (target_function == "dstream.steady_algo.assign_storage_site") {
            process_single_input(S, T,
                steady_algo::steady_has_ingest_capacity,
                steady_algo::steady_assign_storage_site);
        }
        else if (target_function == "dstream.stretched_algo.assign_storage_site") {
            process_single_input(S, T,
                stretched_algo::stretched_has_ingest_capacity,
                stretched_algo::stretched_assign_storage_site);
        }
        else if (target_function == "dstream.tilted_algo.assign_storage_site") {
            process_single_input(S, T,
                tilted_algo::tilted_has_ingest_capacity,
                tilted_algo::tilted_assign_storage_site);
        }
        else {
            std::cerr << "Error: Unknown algorithm function: " << target_function << '\n';
            return false;
        }
    }
    return true;
}

}  // namespace

int main(int argc, char* argv[]) {
    std::signal(SIGPIPE, SIG_IGN);
    std::ios_base::sync_with_stdio(false);

    std::string_view target_function(argv[1]);
    if (!process_algorithm(target_function)) {
        return 1;
    }

    return 0;
}
