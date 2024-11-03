// Copyright 2024 MaidSafe.net limited.
//
// This SAFE Network Software is licensed to you under The General Public License (GPL), version 3.
// Unless required by applicable law or agreed to in writing, the SAFE Network Software distributed
// under the GPL Licence is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied. Please review the Licences for the specific language governing
// permissions and limitations relating to use of the SAFE Network Software.

use lazy_static::lazy_static;
use sn_transfers::{FOUNDATION_PK, GENESIS_PK, NETWORK_ROYALTIES_PK};

lazy_static! {
    /// The node version used during Identify Behaviour.
    pub static ref IDENTIFY_NODE_VERSION_STR: String =
        format!(
            "safe/node/{}/{}",
            get_truncate_version_str(),
            get_key_version_str(),
        );

    /// The client version used during Identify Behaviour.
    pub static ref IDENTIFY_CLIENT_VERSION_STR: String =
        format!(
            "safe/client/{}/{}",
            get_truncate_version_str(),
            get_key_version_str(),
        );

    /// The req/response protocol version
    pub static ref REQ_RESPONSE_VERSION_STR: String =
        format!(
            "/safe/node/{}/{}",
            get_truncate_version_str(),
            get_key_version_str(),
        );

    /// The identify protocol version
    pub static ref IDENTIFY_PROTOCOL_STR: String =
        format!(
            "safe/{}/{}",
            get_truncate_version_str(),
            get_key_version_str(),
        );
}

// Protocol support shall be downward compatible for patch only version update.
// i.e. versions of `A.B.X` or `A.B.X-alpha.Y` shall be considered as a same protocol of `A.B`
fn get_truncate_version_str() -> String {
    let version_str = env!("CARGO_PKG_VERSION");
    let parts = version_str.split('.').collect::<Vec<_>>();
    if parts.len() >= 2 {
        format!("{}.{}", parts[0], parts[1])
    } else {
        panic!("Cannot obtain truncated version str for {version_str:?}: {parts:?}");
    }
}

/// Get the PKs version string.
/// If the public key mis-configed via env variable,
/// it shall result in being rejected to join by the network
pub fn get_key_version_str() -> String {
    let mut f_k_str = FOUNDATION_PK.to_hex();
    let _ = f_k_str.split_off(6);
    let mut g_k_str = GENESIS_PK.to_hex();
    let _ = g_k_str.split_off(6);
    let mut n_k_str = NETWORK_ROYALTIES_PK.to_hex();
    let _ = n_k_str.split_off(6);
    format!("{f_k_str}_{g_k_str}_{n_k_str}")
}
