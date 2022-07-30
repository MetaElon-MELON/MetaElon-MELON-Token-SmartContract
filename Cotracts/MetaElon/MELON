// SPDX-License-Identifier: MIT
pragma solidity ^0.8.14;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Snapshot.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/utils/math/SafeCast.sol";

contract Metaelon is ERC20, ERC20Snapshot, Ownable, Pausable {
    using SafeCast for uint256;
    using SafeCast for int256;
    bool is_taxed;
    uint256 tax_fee = 1;
    uint256 dividend = 100; // set dividend to 100 for int tax, set to 1000 for decimal tax (0.4 example)
    address wallet_fees = 0x16D60ea483c3387667364BFd39C13b7809173E14;
    address[] public excludedFromFees;

    constructor() ERC20("MetaElon", "MELON") {
        _mint(msg.sender, 1000000000 * 10**decimals());
        excludedFromFees.push(msg.sender);
    }

    function transfer(address to, uint256 amount)
        public
        virtual
        override
        returns (bool)
    {
        address owner = _msgSender();
        is_taxed = is_in_excludedFromFees(owner);
        if (is_taxed) {
            uint256 perc = (amount * tax_fee) / dividend; // se vuoi una tax_fee decimale ES: 0.4 , imposta la tax_fee = 4 e dividi per 1000 invece di 100
            amount = amount - perc;
            _transfer(owner, to, amount);
            _transfer(owner, wallet_fees, perc);
        } else {
            _transfer(owner, to, amount);
        }
        return true;
    }

    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) public virtual override returns (bool) {
        address spender = _msgSender();
        is_taxed = is_in_excludedFromFees(spender);
        if (is_taxed) {
            uint256 perc = (amount * tax_fee) / 100;
            amount = amount - perc;
            _spendAllowance(from, spender, amount);
            _transfer(from, to, amount);
            _transfer(from, wallet_fees, perc);
        } else {
            _spendAllowance(from, spender, amount);
            _transfer(from, to, amount);
        }
        return true;
    }

    function add_excludedFromFees(address privilege) public onlyOwner {
        //WARNING, only add function, can't remove
        excludedFromFees.push(privilege);
    }

    function remove_excludedFromFees(uint256 index) public onlyOwner {
        require(excludedFromFees.length > index, "Out of bounds");
        // move all elements to the left, starting from the `index + 1`
        for (uint256 i = index; i < excludedFromFees.length - 1; i++) {
            excludedFromFees[i] = excludedFromFees[i + 1];
        }
        excludedFromFees.pop(); // delete the last item
    }

    function is_in_excludedFromFees(address control)
        internal
        view
        returns (bool)
    {
        for (uint256 i = 0; i < excludedFromFees.length; i++) {
            if (excludedFromFees[i] == control) {
                return false;
            }
        }
        return true;
    }

    function list_excludedFromFees() public view returns (address[] memory) {
        return excludedFromFees;
    }

    function change_walletFees(address substitute) public onlyOwner {
        wallet_fees = substitute;
    }

    function view_walletFees() public view returns (address) {
        return (wallet_fees);
    }

    function modify_tax(uint256 tax, uint256 _dividend) public onlyOwner {
        tax_fee = tax;
        dividend = _dividend;
    }

    function view_tax() public view returns (uint256, uint256) {
        return (tax_fee, dividend);
    }

    function snapshot() public onlyOwner {
        _snapshot();
    }

    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override(ERC20, ERC20Snapshot) whenNotPaused {
        super._beforeTokenTransfer(from, to, amount);
    }
}
