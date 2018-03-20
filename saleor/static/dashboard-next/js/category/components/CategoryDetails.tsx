import DeleteForever from "material-ui-icons/DeleteForever";
import ModeEdit from "material-ui-icons/ModeEdit";
import Button from "material-ui/Button";
import Card, { CardActions, CardContent, CardHeader } from "material-ui/Card";
import IconButton from "material-ui/IconButton";
import Typography from "material-ui/Typography";
import * as React from "react";
import { Link } from "react-router-dom";

import PageHeader from "../../components/PageHeader";
import Skeleton from "../../components/Skeleton";
import i18n from "../../i18n";

interface CategoryDetailsProps {
  backLink?: string;
  description?: string;
  editButtonLink?: string;
  title?: string;
  handleRemoveButtonClick?();
}

export const CategoryDetails: React.StatelessComponent<
  CategoryDetailsProps
> = ({
  backLink,
  description,
  editButtonLink,
  handleRemoveButtonClick,
  title
}) => (
  <Card>
    <PageHeader backLink={backLink} title={title}>
      <IconButton onClick={handleRemoveButtonClick}>
        <DeleteForever />
      </IconButton>
      <IconButton
        component={props => (
          <Link
            to={editButtonLink !== undefined ? editButtonLink : "#"}
            {...props}
          />
        )}
      >
        <ModeEdit />
      </IconButton>
    </PageHeader>
    <CardContent>
      <Typography variant="body1">
        {description !== undefined
          ? description
          : [
              <Skeleton key="skel-1" style={{ width: "80%" }} />,
              <Skeleton key="skel-2" style={{ width: "75%" }} />,
              <Skeleton key="skel-3" style={{ width: "60%" }} />
            ]}
      </Typography>
    </CardContent>
  </Card>
);

export default CategoryDetails;
