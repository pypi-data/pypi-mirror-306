# Changelog

All notable changes to this project will be documented in this file. (from version 13.0.1.1.0 onwards)

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [13.0.1.3.1] - 05-11-2024
### Fix
- corrected name generation for new contracts
- corrected construction of product search string
- contract date now set correctly on new contracts
- corrected product string search generation

## [13.0.1.3.0] - 28-10-2024
### Feature
- Added new endpoint to create contracts 

### Fix
- Changed email that recieves the new contract notification

### Performance
- Limited search of contract products in new contract endpoint to speed up search

## [13.0.1.2.1] - 11-10-2024
### Fixed
-  Append comment instead of overwriting in contacts endpoint

## [13.0.1.2.0] - 24-09-2024
### Added
- Endpoint to allow allocation report download 

### Fixed
- Added missing field 'is_chalet' to contacts endpoint

## [13.0.1.1.14] - 12-06-2024
### Fixed
- Method name

## [13.0.1.1.13] - 23-04-2024
### Added
- Endpoint to return basic buissines metrics

### Fixed
- Added missing field to contracts endpoint

## [13.0.1.1.12] - 02-04-2024
### Fixed
- Removed 'Guardabosques' contracts from list of return contracts

## [13.0.1.1.11] - 06-03-2024
### Added
- Contacts endpoint now supports categories (tags) field

### Fixed
- Country and state asignment in contacts endpoint
- Search when upserting a contat (now done by vat first)
- Corrected operator when searching by vat
- Edge case so vat is not modified if not needed
- Upper case transform to vat

## [13.0.1.1.10] - 07-02-2024
### Performance
- Updated build process to use whool

### Refactor
- Removed limitation of showing contracts for 'Las Naves Brillen'

## [13.0.1.1.9] - 13-12-2023
### Added
- Added endpoint to create contacts

## [13.0.1.1.8] - 28-09-2023

### Added

- Note on contact when rgpd is accepted

## [13.0.1.1.7] - 24-08-2023

### Fixed

- Missing property in allow promotions method

## [13.0.1.1.6] - 08-08-2023

### Added
- New endpoint to retrieve powerstations open for investment

## [13.0.1.1.5] - 05-06-2023

### Added 
- New endpoint to allow synchronization with mailchimp via mailchimp webhooks


## [13.0.1.1.4] - 29-06-2023

### Fixed
- Promotions policy endpoint to allow both subscription and unsubscription

## [13.0.1.1.3] - 09-06-2023

### Added
- Endpoint to update promotions policy of a contact

### Fixed
- Comparator of vat in login and signup to be case insensitive

## [13.0.1.1.2] - 26-04-2023

### Fixed
- User update process
- Password regex to allow symbols

## [13.0.1.1.1] - 20-04-2023

### Fixed
- Selection of contacts on signup request

## [13.0.1.1.0] - 11-04-2023

### Fixed
- Incorrect retrieval of account allocations
- Count of allocations to use correct search domain
- Naming of company users
- Location of a user
- Allocations shown based on check
- Allocation period calculation
- Firsname and lastname of users with two first names

### Removed
- Email validation on users to allow multiple emails separated by ';'
