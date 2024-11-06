.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
	:target: http://www.gnu.org/licenses/agpl
	:alt: License: AGPL-3

=======================================================
Account Invoice Report Grouped By Picking Hide Pickings
=======================================================

This module allows to hide pickings on the account invoice report grouped by pickings


Installation
============

To install this module, you need to:

#. Only install


Configuration
=============

To configure this module, you need to:

#. Only install


Usage
=====

To use this module, you need to:

#. Generate a sales order with a confirmed delivery that needs some correction.
#. Go to a deliverie picking form.
#. Click the return button, mark the 'is internal return check', and make a full return. If you dont return all the moves of the picking, an error will be shown.
#. Edit the sales order, and generate a correct final delivery
#. Generate the invoice of the sales order, and print its report. See how the first picking and its return doesn't appear.
#. In addition, you can manually choose whose stock pickings you want to show going to: Picking Form / Additional Info / Hide on Invoice. If you do it manually, remember that you have to hide all the transaction (a full delivery and a full return).


Bug Tracker
===========

Bugs and errors are managed in `issues of GitHub <https://github.com/sygel-technology/sy-account-invoice-reporting/issues>`_.
In case of problems, please check if your problem has already been
reported. If you are the first to discover it, help us solving it by indicating
a detailed description `here <https://github.com/sygel-technology/sy-account-invoice-reporting/issues/new>`_.

Do not contact contributors directly about support or help with technical issues.


Credits
=======

Authors
~~~~~~~

* Sygel, Odoo Community Association (OCA)


Contributors
~~~~~~~~~~~~

* Alberto Martínez <alberto.martinez@sygel.es>


Maintainer
~~~~~~~~~~

This module is maintained by Sygel.

.. image:: https://pbs.twimg.com/profile_images/702799639855157248/ujffk9GL_200x200.png
   :alt: Sygel
   :target: https://www.sygel.es

This module is part of the `Sygel/sy-account-invoice-reporting <https://github.com/sygel-technology/sy-account-invoice-reporting>`_.

To contribute to this module, please visit https://github.com/sygel.
