import React, { Component } from 'react';
import * as PropTypes from 'prop-types';
import { withRouter, Link } from 'react-router-dom';
import { compose } from 'ramda';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import inject18n from '../../../components/i18n';

const styles = theme => ({
  button: {
    marginRight: theme.spacing(2),
    padding: '2px 5px 2px 5px',
    minHeight: 20,
    textTransform: 'none',
  },
  icon: {
    marginRight: theme.spacing(1),
  },
});

class TopMenuConnectors extends Component {
  render() {
    const { t, location, classes } = this.props;
    return (
      <div>
        <Button
          component={Link}
          to="/dashboard/connectors"
          variant={
            location.pathname === '/dashboard/connectors' ? 'contained' : 'text'
          }
          size="small"
          color={
            location.pathname === '/dashboard/connectors' ? 'primary' : 'inherit'
          }
          classes={{ root: classes.button }}
        >
          {t('Data import')}
        </Button>
        <Button
          component={Link}
          to="/dashboard/connectors/status"
          variant={
            location.pathname === '/dashboard/connectors/status' ? 'contained' : 'text'
          }
          size="small"
          color={
            location.pathname === '/dashboard/connectors/status' ? 'primary' : 'inherit'
          }
          classes={{ root: classes.button }}
        >
          {t('Status')}
        </Button>
      </div>
    );
  }
}

TopMenuConnectors.propTypes = {
  classes: PropTypes.object,
  location: PropTypes.object,
  t: PropTypes.func,
  history: PropTypes.object,
};

export default compose(
  inject18n,
  withRouter,
  withStyles(styles),
)(TopMenuConnectors);
